'''
description: def for extracting content from the docx file
author: allensrj
website: https://github.com/allensrj
'''

import re
import pandas as pd
import numpy as np
from docx import Document
from zhon.hanzi import punctuation


def contains_conditions(text, conditions_list):
    def check_condition(cond, text):
        if isinstance(cond, str):
            return cond in text
        elif isinstance(cond, re.Pattern):
            return bool(cond.search(text))
        return False

    return any(all(check_condition(cond, text) for cond in conditions) for conditions in conditions_list)


def find_chinese_punctuation(text):
    if pd.isna(text):
        return None
    found_punctuation = [char for char in str(text) if char in punctuation]
    return ' '.join(found_punctuation) if found_punctuation else None


def extract_content(path, conditions_list, title_split, language):
    # ---------- extract table part ----------
    if path:
        table_doc = Document(path)
        table_paragraphs_data = []
        for paragraph in table_doc.paragraphs:
            italic_found = any(run.font.italic for run in paragraph.runs if run.font.italic is not None)
            bold_found = any(run.font.bold for run in paragraph.runs if run.font.bold is not None)
            table_paragraphs_data.append({
                "Text": paragraph.text,
                "Style": paragraph.style.name,
                "Italic": italic_found,
                "Bold": bold_found
            })

        table = pd.DataFrame(table_paragraphs_data)

        table = table[table['Text'] != '']
        table = table[~table['Style'].str.contains('toc')]
        table = table[~table['Italic'] == True]

        # mark the order of the tables
        table.reset_index(drop=True, inplace=True)
        table['ord'] = 0
        flag_count = 0
        for index, row in table.iterrows():
            if contains_conditions(row['Text'], conditions_list):
                flag_count += 1
                table.at[index, 'ord'] = flag_count

        table['ord'] = table['ord'].replace(0, np.nan).ffill().fillna(0).infer_objects().astype(int)
        table = table[table['ord'] != 0]

        # delete the rows with multiple headings
        table['Heading_count'] = 0
        for ord, group in table.groupby('ord'):
            if ord == 0:
                continue
            count = 0
            for index, row in group.iterrows():
                if "Heading" in row['Style']:
                    count += 1
                    table.at[index, 'Heading_count'] = count
        table = table[table['Heading_count'] <= 1]

        if not any('Heading' in style for style in table['Style']):
            print(f'WARNING: No Heading style found in {path}')

        # mark table and footnote, generate Type
        for index, row in table.iterrows():
            if contains_conditions(row['Text'], conditions_list):
                table.at[index, 'Type'] = 'Table'
            else:
                table.at[index, 'Type'] = 'Footnote'

        # delete rows of bold in type=footenote,
        table = table[~((table['Type'] == 'Footnote') & (table['Bold'] == True))]

        # aggregate footnotes
        footnote_aggregation = table[table['Type'] == 'Footnote'].groupby('ord')['Text'].agg(lambda texts: '\\line '.join(texts))
        table = table.merge(footnote_aggregation, on='ord', how='left', suffixes=('', '_aggregated'))

        table['Text_aggregated'] = table['Text_aggregated'].str.strip()
        table['Text_aggregated'] = table['Text_aggregated'].replace(r'\\line$', '', regex=True).replace(r'^\\line$', '', regex=True)

        table['Text_aggregated'] = table['Text_aggregated'].fillna('').astype(str).str.strip()
        table['Text_aggregated'] = table['Text_aggregated'].replace(r'\\line$', '', regex=True).replace(r'^\\line$', '', regex=True)

        table['Text'] = table['Text'].str.replace(f'{title_split}', '\\line')


        if table['Text'].str.startswith('\\line').any():
            print(f'WARNING: {path} file has a line starting with \\line, which can cause issues in the output file')

        # keep Type = Table
        table = table[table['Type'] == 'Table']
        table.drop(columns=['Type'], inplace=True)

        # split the table titles into columns
        table['line_count'] = table['Text'].str.count('\\\\line')
        max_lines = table['line_count'].max()
        columns = [f'col{i+1}' for i in range(max_lines + 1)]
        table[columns] = table['Text'].str.split('\\\\line', expand=True, n=max_lines)

        if language == 'EN':
            table['Output_Type'] = table['col1'].apply(
                lambda x: 'T' if 'TABLE' in x.upper() else ('L' if 'LISTING' in x.upper() else ('F' if 'FIGURE' in x.upper() else '')))
        elif language == 'CN':
            table['Output_Type'] = table['col1'].apply(
                lambda x: '列表' if '列表' in x else ('表' if '表' in x else ('图' if '图' in x else '')))

        table['Output_Number'] = table['col1'].apply(
            lambda x: re.search(r'^[^\d]*[\d\.x]+[^\s]*', x).group() if re.search(r'^[^\d]*[\d\.x]+[^\s]*', x) else '')
        table['Output_Number'] = table.apply(
            lambda row: (
                row['Output_Number'].upper()
                .replace('TABLE', '').strip() if row['Output_Type'] == 'T' else
                row['Output_Number'].upper()
                .replace('LISTING', '').strip() if row['Output_Type'] == 'L' else
                row['Output_Number'].upper()
                .replace('FIGURE', '').strip() if row['Output_Type'] == 'F' else
                row['Output_Number']
                .replace('表', '').strip() if row['Output_Type'] == '表' else
                row['Output_Number']
                .replace('列表', '').strip() if row['Output_Type'] == '列表' else
                row['Output_Number']
                .replace('图', '').strip() if row['Output_Type'] == '图' else
                row['Output_Number']
            ),
            axis=1
        )

        if max_lines > 2:
            title_columns = [f'col{i+1}' for i in range(1, max_lines)]
            table['Titles'] = table[title_columns].apply(lambda x: '\\line'.join(x.dropna()), axis=1)
        elif max_lines == 1:
            table['Titles'] = table['col2']
        elif max_lines == 2:
            table['Titles'] = table['col2']
        else:
            table['Titles'] = table['col1']


        table['Population'] = table.apply(lambda row: row[f'col{row.line_count + 1}'], axis=1)
        table['Footnotes'] = table['Text_aggregated']

        if table[f'col{max_lines+1}'].isnull().all().all():
            print(f'WARNING: {path} has one more \line of the end of the titles, which can cause issues in the output file')

        table = table[['Output_Type', 'Output_Number', 'Titles', 'Population', 'Footnotes']]

        table['Chinese_Punctuation_Found'] = table['Footnotes'].apply(find_chinese_punctuation)

    else:
        table = pd.DataFrame(columns=['Output_Type', 'Output_Number', 'Titles', 'Population', 'Footnotes', 'Chinese_Punctuation_Found'])

    return table
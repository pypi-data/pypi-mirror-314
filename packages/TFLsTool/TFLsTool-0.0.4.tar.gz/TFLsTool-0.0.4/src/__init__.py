'''
description: TFLs Tools Collection.
author: allensrj
website: https://github.com/allensrj/TFLsTool
'''


import os
import re
import time
import math
from datetime import datetime
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from openpyxl import load_workbook
from .ExtractShellToTracker import *
from .CompletenessReport import *
from .CombineRTF import chinese_to_rtf


def extract_shell_to_tracker(table_path, table_conditions_list, listing_path, listing_conditions_list, figure_path, figure_conditions_list, title_split, language, output_path):

    if not table_path and not listing_path and not figure_path:
        print("WARNING: Input the correct file path. If a file is unnecessary, set the path parameter as None")
        return

    if not table_conditions_list and not listing_conditions_list and not figure_conditions_list:
        print("WARNING: Please enter the required conditions. You can find detailed instructions on adding conditions at allensrj.github.io")
        return

    if not title_split:
        print("WARNING: Please enter the title split.")
        return

    if not language:
        print("WARNING: Please enter the language.")
        return

    if not output_path:
        print("WARNING: Input the correct output path.")
        return

    try:
        table = extract_content(table_path, table_conditions_list, title_split, language)
    except Exception as e:
        print(f'Error: {e}')
    try:
        listing = extract_content(listing_path, listing_conditions_list, title_split, language)
    except Exception as e:
        print(f'Error: {e}')
    try:
        figure = extract_content(figure_path, figure_conditions_list, title_split, language)
    except Exception as e:
        print(f'Error: {e}')

    df = pd.concat([table, listing, figure], axis=0)
    df.to_excel(output_path, index=False)
    wb = load_workbook(output_path)
    ws = wb.active

    for col in ws.columns:
        column = col[0].column_letter
        ws.column_dimensions[column].width = 30

    wb.save(output_path)

    print('Output file generated')


def completeness_report(
        file_path,
        sheet_name,
        ds_select_list,
        ds_status_list,
        project,
        side,
        email_sender,
        email_recipient,
        email_cc,
        outpath=os.popen('echo $HOME').read().strip()
    ):
    required_params = {
        "file_path": file_path,
        "sheet_name": sheet_name,
        "ds_select_list": ds_select_list,
        "ds_status_list": ds_status_list,
        "project": project,
        "side": side,
        "email_sender": email_sender,
        "email_recipient": email_recipient,
        "email_cc": email_cc
    }
    for param_name, param_value in required_params.items():
        if param_value is None or (isinstance(param_value, str) and param_value == ""):
            raise ValueError(f"{param_name} -- Parameter can not be empty, please fill in the correct value")

    time = datetime.now().strftime('%Y-%m-%d')

    try:
        df = pd.read_excel(file_path, sheet_name=f'{sheet_name}')
    except ValueError:
        print('TLFs sheetname not exist.')

    try:
        df = df[ds_select_list]
    except ValueError as e:
        print(e)

    # ------------------- Production -------------------
    df_all = df.groupby(f'{ds_select_list[1]}')[f'{ds_select_list[1]}'].count().reset_index(name='all')
    df_sum = df.groupby([f'{ds_select_list[1]}', f'{ds_select_list[0]}'])[f'{ds_select_list[0]}'].count().reset_index(name='sum')
    df_sum = df_sum.pivot_table(index=f'{ds_select_list[1]}', columns=f'{ds_select_list[0]}', values='sum',
                                fill_value=0).reset_index()

    expected_cols = ['F', 'T', 'L']
    existing_cols = df_sum.columns.tolist()
    for col in expected_cols:
        if col not in existing_cols:
            df_sum[col] = 0

    df_sum['F'] = df_sum['F'].astype(int)
    df_sum['T'] = df_sum['T'].astype(int)
    df_sum['L'] = df_sum['L'].astype(int)

    df_sum.rename(columns={'F': 'F_sum', 'T': 'T_sum', 'L': 'L_sum'}, inplace=True)

    # TFL count
    df_count = df.groupby([f'{ds_select_list[1]}',
                           f'{ds_select_list[0]}',
                           f'{ds_select_list[2]}'])[f'{ds_select_list[0]}'].value_counts().reset_index(name='count')
    df_count = df_count[
        (df_count[f'{ds_select_list[2]}'] == f'{ds_status_list[0]}') | (df_count[f'{ds_select_list[2]}'].isna())]
    df_count = df_count.pivot_table(index=[f'{ds_select_list[1]}', f'{ds_select_list[2]}'],
                                    columns=f'{ds_select_list[0]}', values='count', fill_value=0).reset_index()

    expected_cols = ['F', 'T', 'L']
    existing_cols = df_count.columns.tolist()
    for col in expected_cols:
        if col not in existing_cols:
            df_count[col] = 0

    df_count['F'] = df_count['F'].astype(int)
    df_count['T'] = df_count['T'].astype(int)
    df_count['L'] = df_count['L'].astype(int)

    df_count.rename(columns={'F': 'F_count', 'T': 'T_count', 'L': 'L_count'}, inplace=True)

    df_final = pd.merge(df_all, df_sum, on=f'{ds_select_list[1]}', how='left')
    df_final = pd.merge(df_final, df_count, on=f'{ds_select_list[1]}', how='left')
    df_final.fillna(0, inplace=True)
    print(df_final)

    # ------------------- Production create figure -------------------
    N = len(df_final)
    ind = np.arange(N)
    width = 0.2

    fig, ax = plt.subplots(figsize=(20, 8))

    bars1 = ax.barh(ind - width, df_final['F_count'], width, label='Figures', color='#90EE90')
    bars2 = ax.barh(ind, df_final['L_count'], width, label='Listings', color='#87CEFA')
    bars3 = ax.barh(ind + width, df_final['T_count'], width, label='Tables', color='#FFA07A')

    ax.set_xlabel('Number of tasks ', fontsize=14, fontweight='bold')
    ax.set_title(f'{project} Completeness of Production', fontsize=36, fontweight='bold')

    y_labels = [f"{sp} \n({total})" for sp, total in zip(df_final[f'{ds_select_list[1]}'], df_final['all'])]
    ax.set_yticks(ind)
    ax.set_yticklabels(y_labels, fontsize=14, rotation=0, ha='right', fontweight='bold')
    legend = ax.legend(fontsize=12, handlelength=2)

    for i in range(N):
        F_percent = (df_final['F_count'][i] / df_final['F_sum'][i]) * 100 if df_final['F_sum'][i] != 0 else 0
        L_percent = (df_final['L_count'][i] / df_final['L_sum'][i]) * 100 if df_final['L_sum'][i] != 0 else 0
        T_percent = (df_final['T_count'][i] / df_final['T_sum'][i]) * 100 if df_final['T_sum'][i] != 0 else 0
        ax.text(df_final['F_count'][i] + 0.5, ind[i] - width,
                f"{df_final['F_count'][i]} / {df_final['F_sum'][i]} ({F_percent:.1f}%)", va='center', fontsize=14,
                fontweight='bold')
        ax.text(df_final['L_count'][i] + 0.5, ind[i],
                f"{df_final['L_count'][i]} / {df_final['L_sum'][i]} ({L_percent:.1f}%)", va='center', fontsize=14,
                fontweight='bold')
        ax.text(df_final['T_count'][i] + 0.5, ind[i] + width,
                f"{df_final['T_count'][i]} / {df_final['T_sum'][i]} ({T_percent:.1f}%)", va='center', fontsize=14,
                fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{outpath}/producion.png')
    plt.close()
    print('Production side generated sucessfully.')

    # ------------------- QC -------------------
    qc_all = df.groupby(f'{ds_select_list[3]}')[f'{ds_select_list[3]}'].count().reset_index(name='all')
    qc_sum = df.groupby([f'{ds_select_list[3]}', f'{ds_select_list[0]}'])[f'{ds_select_list[0]}'].count().reset_index(name='sum')
    qc_sum = qc_sum.pivot_table(index=f'{ds_select_list[3]}', columns=f'{ds_select_list[0]}', values='sum',
                                fill_value=0).reset_index()

    expected_cols = ['F', 'T', 'L']
    existing_cols = qc_sum.columns.tolist()
    for col in expected_cols:
        if col not in existing_cols:
            qc_sum[col] = 0

    qc_sum['F'] = qc_sum['F'].astype(int)
    qc_sum['T'] = qc_sum['T'].astype(int)
    qc_sum['L'] = qc_sum['L'].astype(int)

    qc_sum.rename(columns={'F': 'F_sum', 'T': 'T_sum', 'L': 'L_sum'}, inplace=True)

    # QC count
    qc_count = df.groupby([f'{ds_select_list[3]}',
                           f'{ds_select_list[0]}',
                           f'{ds_select_list[4]}'])[f'{ds_select_list[0]}'].value_counts().reset_index(name='count')
    qc_count = qc_count[
        (qc_count[f'{ds_select_list[4]}'] == f'{ds_status_list[1]}') | (qc_count[f'{ds_select_list[4]}'].isna())]
    qc_count = qc_count.pivot_table(index=[f'{ds_select_list[3]}', f'{ds_select_list[4]}'],
                                    columns=f'{ds_select_list[0]}', values='count', fill_value=0).reset_index()

    expected_cols = ['F', 'T', 'L']
    existing_cols = qc_count.columns.tolist()
    for col in expected_cols:
        if col not in existing_cols:
            qc_count[col] = 0

    qc_count['F'] = qc_count['F'].astype(int)
    qc_count['T'] = qc_count['T'].astype(int)
    qc_count['L'] = qc_count['L'].astype(int)

    qc_count.rename(columns={'F': 'F_count', 'T': 'T_count', 'L': 'L_count'}, inplace=True)

    qc_final = pd.merge(qc_all, qc_sum, on=f'{ds_select_list[3]}', how='left')
    qc_final = pd.merge(qc_final, qc_count, on=f'{ds_select_list[3]}', how='left')
    qc_final.fillna(0, inplace=True)
    print(qc_final)

    # ------------------- QC create figure -------------------
    N = len(qc_final)
    ind = np.arange(N)
    width = 0.2

    fig, ax = plt.subplots(figsize=(20, 8))

    bars1 = ax.barh(ind - width, qc_final['F_count'], width, label='Figures', color='#90EE90')
    bars2 = ax.barh(ind, qc_final['L_count'], width, label='Listings', color='#87CEFA')
    bars3 = ax.barh(ind + width, qc_final['T_count'], width, label='Tables', color='#FFA07A')

    ax.set_xlabel('Number of tasks ', fontsize=14, fontweight='bold')
    ax.set_title(f'{project} Completeness of QC', fontsize=36, fontweight='bold')

    y_labels = [f"{sp} \n({total})" for sp, total in zip(qc_final[f'{ds_select_list[3]}'], qc_final['all'])]
    ax.set_yticks(ind)
    ax.set_yticklabels(y_labels, fontsize=14, rotation=0, ha='right', fontweight='bold')
    legend = ax.legend(fontsize=12, handlelength=2)

    for i in range(N):
        F_percent = (qc_final['F_count'][i] / qc_final['F_sum'][i]) * 100 if qc_final['F_sum'][i] != 0 else 0
        L_percent = (qc_final['L_count'][i] / qc_final['L_sum'][i]) * 100 if qc_final['L_sum'][i] != 0 else 0
        T_percent = (qc_final['T_count'][i] / qc_final['T_sum'][i]) * 100 if qc_final['T_sum'][i] != 0 else 0
        ax.text(qc_final['F_count'][i] + 0.5, ind[i] - width,
                f"{qc_final['F_count'][i]} / {qc_final['F_sum'][i]} ({F_percent:.1f}%)", va='center', fontsize=14,
                fontweight='bold')
        ax.text(qc_final['L_count'][i] + 0.5, ind[i],
                f"{qc_final['L_count'][i]} / {qc_final['L_sum'][i]} ({L_percent:.1f}%)", va='center', fontsize=14,
                fontweight='bold')
        ax.text(qc_final['T_count'][i] + 0.5, ind[i] + width,
                f"{qc_final['T_count'][i]} / {qc_final['T_sum'][i]} ({T_percent:.1f}%)", va='center', fontsize=14,
                fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{outpath}/qc.png')
    plt.close()
    print('QC side generated sucessfully.')

    # ------------------- Generate Completeness png -------------------
    if side == 'all':
        img1 = Image.open(f'{outpath}/producion.png')
        img2 = Image.open(f'{outpath}/qc.png')

        width1, height1 = img1.size
        width2, height2 = img2.size
        spacing = 200
        total_height = height1 + height2 + spacing
        max_width = max(width1, width2)
        new_img = Image.new('RGB', (max_width, total_height), (255, 255, 255))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (0, height1 + spacing))

        new_img.save(f'{outpath}/completeness_{time}.png')
        os.remove(f'{outpath}/producion.png')
        os.remove(f'{outpath}/qc.png')
        print('all side completeness picture generated sucessfully.')
    elif side == 'p':
        img1 = Image.open(f'{outpath}/producion.png')
        img1.save(f'{outpath}/completeness_{time}.png')
        os.remove(f'{outpath}/producion.png')
        print('Production side completeness picture generated sucessfully.')
    elif side == 'q':
        img2 = Image.open(f'{outpath}/qc.png')
        img2.save(f'{outpath}/completeness_{time}.png')
        os.remove(f'{outpath}/qc.png')
        print('QC side completeness picture generated sucessfully.')
    else:
        print("Invalid side parameter value. Accepted values are 'all', 'p', or 'q'.")
        return

    # ------------------- Send Email -------------------
    subject = f'{project} Completeness Report'
    body = f'{project} Completeness Report:'
    image_path = f'{outpath}/completeness_{time}.png'

    send_email(email_sender, email_recipient, email_cc, subject, body, image_path)


def combine_rtf(srcpath, inclist, exclist, addtoc, row_of_toc_in_a_page, tocfile, outpath, outfile):
    start_time = time.time()

# Grab the rtf in the path to form an intermediate dataset
    files = pd.DataFrame()
    for path in srcpath:
        file_list = [f for f in os.listdir(path) if f.endswith('.rtf')]
        paths = [path] * len(file_list)
        files = pd.concat(
            [files, pd.DataFrame({'name': file_list, 'path': paths})],
            ignore_index=True
        )

# Merge tocfile
    if tocfile is not None:
        tocfile = pd.read_excel(tocfile, sheet_name='Sheet1')
        if tocfile.empty:
            print("WARNING: tocfile is empty, please check!\n")
        tocfile['filename'] = tocfile['filename'].apply(lambda x: x + '.rtf')
        tocfile['ord'] = tocfile.index + 1

        merge = pd.merge(files, tocfile, how='outer', left_on='name', right_on='filename')
        if merge['name'].isnull().sum() > 0 :
            print("WARNING: Mismatch between tocfile and folders, the files required in the table of contents (TOC) may be missing, please check!\n")
        if merge['filename'].isnull().sum() > 0:
            print("WARNING: Mismatch between tocfile and folders. Maybe everything going well, please make sure that the files required by the table of contents (TOC) may exist in the folder.\n")
        merge = merge[~merge['filename'].isnull()]
    else:
        merge = files
        merge['ord'] = merge['name'].apply(
            lambda x: 1 if x.startswith("t") else 2 if x.startswith("f") else 3 if x.startswith("l") else None
        )
        merge['filename'] = merge['name']

    merge.sort_values(by=['ord', 'name'], inplace=True)
    merge.reset_index(drop=True, inplace=True)


# inclist, exclist
    if inclist:
        merge = merge[merge['filename'].str.contains(inclist)]
    if exclist:
        merge = merge[~merge['filename'].str.contains(exclist)]

    merge.reset_index(drop=True, inplace=True)
    merge = merge.copy()
    merge['order'] = merge.index + 1


    page_add = math.ceil(len(merge['filename']) / row_of_toc_in_a_page)

# Grab the title and page of the rtf file
    title = []
    content = ""
    for i in range(len(merge['filename'])):
        if str(merge['path'][i]) != 'nan':
            with open(
                str(merge['path'][i]) + "/" + str(merge['filename'][i]), 'r', encoding='latin-1'
            ) as file:
                prev_line, idx_line, next_line = None, None, None
                for line in file:
                    if 'IDX' in line:
                        idx_line = line.strip()
                        break
                    prev_line = line.strip()

                if idx_line is not None:
                    try:
                        next_line = next(file).strip()
                    except StopIteration:
                        pass

                if idx_line:
                    content += f"Previous Line: {prev_line if prev_line else 'N/A'}\n"
                    content += f"IDX Line: {idx_line}\n"
                    content += f"Next Line: {next_line if next_line else 'N/A'}\n"
                    content += "\n"

                    content = content.split(r"\line{}")[0]
                    content = content.split(r"\s999 \b ")[1]
                    content = content.split(r"\b")[0]
                    content = content.replace(r"\line", " ")
                    content = re.sub(r'\s+', ' ', content)
                else:
                    content = f"IDX not found, ERROR in {merge['name'][i]}"
                    print(f"IDX not found, ERROR in {merge['name'][i]}")
        else:
            content = ''
        title.append(content)


    title = [i.strip() for i in title]
    for i in range(len(title)):
        title[i] = f"{{\\cf0\\b {title[i]} \\b0\\tab}}"
    merge['title'] = title

    page_lines = []
    for i in range(len(merge['name'])):
        found_page_line = False
        if str(merge['path'][i]) != 'nan':
            with open(
                merge['path'][i] + "/" + merge['name'][i], 'r', encoding='latin-1'
            ) as file:
                for li in file:
                    if 'Page 1{ of' in li:
                        page_line = li.strip()
                        page_lines.append(page_line)
                        found_page_line = True
                        break
                if not found_page_line:
                    page_lines.append('notfound')
                    print(f"Page number not found, ERROR in {merge['name'][i]}")
        else:
            page_lines.append('')

    page_lines = [i.replace(" ", "") for i in page_lines]
    merge['page'] = page_lines
    merge['page'] = merge['page'].apply(lambda x: x.split('{Page1{of')[1] if '{' in x else x)
    merge['page'] = merge['page'].apply(lambda x: re.sub(r'\D', '', x))
    merge['page'] = merge['page'].apply(lambda x: int(x) if x else 0)
    merge['page1'] = merge['page'].cumsum().shift(1).fillna(0).astype(int)
    merge['page_num'] = merge['page1'] + 1
    merge['page_num'] = merge['page1'] + 1 + page_add
    merge.drop(columns=['page1'], inplace=True)


# generate the body of the rtf file
    merge_body = merge.copy()
    merge_body = merge_body[merge_body['path'].notnull()]
    merge_body.reset_index(drop=True, inplace=True)
    merge_body['body_ord'] = merge_body.index + 1

    content = ""
    for i in range(len(merge_body['name'])):
        text = ""
        with open(merge_body['path'][i] + "/" + merge_body['name'][i], 'r') as f:
            text = f.read()
        text = "\widowctrl" + text.split("\widowctrl")[1]
        text = text.rstrip()
        text = text[:-1]
        text = text.replace("IDX", f"IDX{merge_body['order'][i]}")
        if merge_body['body_ord'][i] == len(merge_body['name']):
            content += text
        else:
            content += text + '\sect'

    with open(merge_body['path'][0] + "/" + merge_body['name'][0], 'r') as f:
        text = f.read()
    header = text.split("\widowctrl")[0]

# generate the toc of the rtf file
    if tocfile is None:
        toc = (
            "\\sectd\\linex0\\endnhere\\pgwsxn15840\\pghsxn12240\\lndscpsxn\\pgnrestart"
            "\\pgnstarts1\\headery1440\\footery1440\\marglsxn1440\\margrsxn1440\\margtsxn1440"
            "\\margbsxn1440\n"
            "\\qc\\f36\\b\\s0{\\s999 Table of Contents \\par}\\s0\\b0\\par\\par\\pard\n"
        )

        current_page_rows = 0
        for i in range(len(merge['title'])):
            toc += (
                f"\\fi-2000\\li2000{{\\f1\\fs18\\cf0{{\\field{{\\*\\fldinst {{ HYPERLINK \\\\l \"IDX{merge['order'][i]}\"}}}}{{\\fldrslt" + merge['title'][i] + "}}" +
                '\n' +
                f"\\ptabldot\\pindtabqr{{\\field{{ {merge['page_num'][i]} }}}}}}\\s0\\par" +
                '\n'
            )
            current_page_rows += 1
            if current_page_rows >= row_of_toc_in_a_page:
                toc += "\\pard\\sect"
                current_page_rows = 0

        toc += "\\pard\\sect"
    else:
        merge['title1'] = merge['toc'].apply(chinese_to_rtf)
        toc = (
            "\\sectd\\linex0\\endnhere\\pgwsxn15840\\pghsxn12240\\lndscpsxn\\pgnrestart"
            "\\pgnstarts1\\headery1440\\footery1440\\marglsxn1440\\margrsxn1440\\margtsxn1440"
            "\\margbsxn1440\n"
            "\\qc\\f36\\b\\s0{\\s999 Table of Contents \\par}\\s0\\b0\\par\\par\\pard\n"
        )

        current_page_rows = 0
        for i in range(len(merge['title'])):
            toc += (
                f"\\fi-2000\\li2000{{\\f1\\fs18\\cf0{{\\field{{\\*\\fldinst {{ HYPERLINK \\\\l \"IDX{merge['order'][i]}\"}}}}{{\\fldrslt" + merge['title1'][i] + "}}" +
                '\n' +
                f"\\ptabldot\\pindtabqr{{\\field{{ {merge['page_num'][i]} }}}}}}\\s0\\par" +
                '\n'
            )
            current_page_rows += 1
            if current_page_rows >= row_of_toc_in_a_page:
                toc += "\\pard\\sect"
                current_page_rows = 0

        toc += "\\pard\\sect"

    con = header + toc + content + "}" if addtoc == "Y" else header + content + "}"
    with open(f'{outpath}/{outfile}.rtf', 'w') as f:
        f.write(con)

    print('Combine finished!\n')

    end_time = time.time()
    print(f"Time Used: {round(end_time - start_time, 1)}s\n")

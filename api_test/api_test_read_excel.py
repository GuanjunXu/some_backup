import xlrd
import random

def rdExcel(fileName):
    xl_data = xlrd.open_workbook(fileName)
    sheet_list = xl_data.sheets()
    all_item = []
    for sh in sheet_list:
        if sheet_list.index(sh) < 2:
            continue
        resource,method = '',''
        mine,param = [],{}
        for row in range(sh.nrows): # add necessity logic
            if row == 0:
                continue
            if sh.row_values(row)[0] != '':
                resource,method = sh.row_values(row)[0],sh.row_values(row)[1]
                mine.append(resource)
                mine.append(method)
            name,necessity = sh.row_values(row)[2],sh.row_values(row)[4]
            val = str(sh.row_values(row)[5]).split(',')
            ran_val = random.choice(val)
            param[name] = ran_val
        mine.append(param)
        all_item.append(mine)
    return all_item

rt = rdExcel('APIcase.xlsx')

f=file('alllllll.txt','w')
f.writelines(str(rt))
f.close()
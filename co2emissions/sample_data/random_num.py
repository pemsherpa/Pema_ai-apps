import random
import xlsxwriter as xls

col = 0
workbook  = xls.Workbook('sample_60_month_data.xlsx')
worksheet  = workbook.add_worksheet()
scope1_cats = ["stationary combustion", "mobile sources", "refrigeration", "fire suppression", "purchased gases"]
scope2_cats = ["electricity", "steam"]
scope3_cats = ["waste", "business travel", "commuting", "upstream distribution"]
scope_cats = scope1_cats + scope2_cats + scope3_cats

def write_header(scope_cats):
     worksheet.write_row(0, 0, scope_cats)

def get_data_for_scope(col, scope_cat):
    print("col = " + str(col))
    scope_data = random.sample(range(1, 10000), 60)
    scope_data.sort()
    print("scope_data = " + str(scope_data))
    worksheet.write_column(1, col, scope_data)
    col = col + 1        

write_header(scope_cats)

for i in range(1, 4, 1):
     print (" i = " + str(i))
     if i == 1:
         for cat in scope1_cats:
             get_data_for_scope(col, cat)
             col = col +1
     elif i == 2:
         for cat in scope2_cats:
             get_data_for_scope(col, cat)
             col = col +1
     else:
          for cat in scope3_cats:
              get_data_for_scope(col, cat) 
              col = col +1

workbook.close()
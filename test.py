from openpyxl import load_workbook
import sys

if sys.argv[-1] == sys.argv[0]:
    print("쿼리 시트가 입력되지 않았습니다.")
    print("사용 방법은 main.py [쿼리 시트 명]입니다. 다시 시도해주세요")
elif len(sys.argv) >= 3:
    print("쿼리 시트 지정이 정확하지 않습니다.")
    print("입력된 매개 변수의 수가", len(sys.argv) - 1, "개입니다.")
    print("쿼리 시트 지정을 하나로 지정해주세요.")
else:
    fileName = sys.argv[1]
    queryPath = "queries/" + fileName + '.xlsx'
    queries = load_workbook(queryPath, data_only=True)
    queriesSheet = queries['시트1']
    queriesSheet.delete_rows(0)
    for row in queriesSheet.rows:
        print(row[0].value, row[1].value)
from slack_sdk import WebClient

# Slack Token
slack_token = '---' # 크롤링 파일을 업로드할 slack token값 직접 입력
client = WebClient(token=slack_token)

# file upload
def upload(Channel, File, Filename, Filetype):
    xlsx_upload = client.files_upload(channels=Channel,         # 업로드할 채널명
                                          file=File,            # 업로드할 파일명
                                          filename=Filename,    # Slack에 올라갈 파일명(확장자명)
                                          filetype=Filetype)    # 업로드할 파일의 타입

# 예시)
# example_xlsx_1 = client.files_upload(channels='crawling_test',
#                                           file='crawling_test.xlsx',
#                                           filename='아프니까사장이다(강남구)_20240421.xlsx',
#                                           filetype='xlsx')
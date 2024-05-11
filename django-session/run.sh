lsof -t -i tcp:8000 | xargs kill -9
# 8000 포트를 사용하는 모든 tcp 연결을 식별하고 해당하는 프로세스 id를 얻어 이를 kill -9 명령어를 사용하여 강제로 종료
python manage.py runserver 127.0.0.1:8000

# sh run.sh로 사용
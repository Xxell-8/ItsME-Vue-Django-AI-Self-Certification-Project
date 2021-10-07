# Porting Manual

## 개발환경

#### Deploy Server

- Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-1018-aws x86_64)

#### DB

- SQLite3 : 3.31.1

#### Front-end

- Vue
  - Vue.js :
  - Vue/Cli : 4.5.13

#### Back-end

- Python : 3.8.10
- Django
  - Django : 3.2.7
  - Django rest framework : 3.12.4
- pip : 20.0.2

#### IDE

- Visual Studio Code : 1.60.2



## 배포 시 특이사항

- https://j5a204.p.ssafy.io/
- 관리자 계정 
  - 이메일 : admin@admin.com
  - 비밀번호 : qwerasdf1
- PuTTY와 WinSCP를 사용하여 배포
- Frontend는 Nginx, Backend는 Gunicorn WSGI server 사용
- 권한의 경우 패키지 설치, 콘솔 이용 관리자 계정 생성 등 콘솔에서 작업 시 ubuntu 계정, 실제 서비스에서 요청 보낼 때는 deploy 계정에 권한을 주어야 합니다. (db 등 권한 문제 방지)
- 보안 연결(HTTPS)은 certbot 이용 (https://certbot.eff.org/)

- 배포 서비스 재시작 명령어

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

- 서비스 경로

```bash
/srv/S05P21A204/
```

- Nginx 설정 파일

```bash
/etc/nginx/sites-available/its_me.conf
```

- Gunicorn 설정 파일

```bash
/etc/systemd/system/gunicorn.service
```



## 외부 서비스

#### 얼굴인식 및 포즈인식 - Tensorflow

- tensorflow.js : 3.9.0
- tensorflow.js-blazeface : 0.0.7
- tensorflow.js-posenet : 2.2.2

#### 글자 인식 - Tesseract

- tesseract-ocr : 4.1.1-2build2
- tesseract-ocr-kor : 1:4.00~git30-7274cfa-1

#### 배포

- AWS
- PuTTY : Release 0.76
- WinSCR : 5.19.2 (build 11614)

- nginx : 1.18.0-0ubuntu1.2
- gunicorn : 20.1.0



## 데이터베이스



## 시연 시나리오




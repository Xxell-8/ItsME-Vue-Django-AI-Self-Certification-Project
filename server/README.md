# SERVER

## 👨‍ Developer

- 권기웅 : Info App, Tesseract 담당
- 이경민 : Accounts App, AWS 배포 및 유지보수 담당



## 📑 사용 기술 & 환경

- Django web framework
- Django rest framework
- JWT Token
- Tesseract OCR



## 💡 IDEA

```
It's Me : 본인 인증 통합 솔루션
```

## 

## 📑 Accounts App

### 📃 회원 관리

- 파트너(기업) 및 실무자 회원으로 나누어 관리
- 각 회원은 고유의 email을 가짐
- 각 파트너는 고유의 코드를 가짐
- 파트너 코드를 통해 소속 기업 구분
- email과 비밀번호를 사용하여 로그인

### 💻 개발 과정

#### 회원가입&로그인

> 실무자 회원가입 및 로그인

dj-rest-auth와 django-allauth 패키지를 이용하여 구현하였습니다.

BaseUserManager를 상속시킨 CustomUserManager를 작성하여, 회원가입과 로그인 시 email과 password를 사용하도록 설정하였고, username, first_name, last_name 필드는 비활성화하였습니다. 

회원가입 시 회사명과 코드를 입력해 일치하는 경우에만 가입이 가능합니다. 

인증의 경우 djangorestframework-simplejwt 패키지를 이용하여 access token, refresh token을 구현하였습니다.

#### 비밀번호 변경 & 프로필 수정 & 회원 탈퇴

> 사용자의 비밀번호 혹은 프로필 수정, 회원 탈퇴

비밀번호 변경의 경우 serializers.py의 클래스 ChangePasswordSerializer를 정의하였고, views.py의 클래스형 뷰인 ChangePasswordView를 정의해 patch 메소드를 통해 검증 및 업데이트를 하도록 구현하였습니다.

프로필 수정의 경우 serializers.py의 클래스 UpdateProfileSerializer를 정의하여 ModelSerializer를 상속받고, User모델을 참조하도록 하였고, update 함수를 정의해 수정하도록 하였습니다. views.py의 클래스형 뷰인 UpdateProfileView를 정의하여 UpdateProfileSerializer를 사용하도록 구현하였습니다.

회원 탈퇴의 경우 주소를 통해 pk를 받도록 하였고, POST 메소드를 이용해 db에서 해당 pk의 사용자 객체를 삭제하도록 하였습니다. 

#### 프로필 및 실무자 리스트 및 가입 대기중 리스트 조회

> 각각의 프로필 조회, 해당 파트너의 실무자 리스트 조회, 가입 대기자 리스트 조회

url로부터 입력받은 pk 혹은 회사코드를 이용하여 db를 조회 혹은 필터링하여, 해당하는 프로필 혹은 실무자 리스트를 불러오도록 구현하였습니다. 또한 현재 유저가 파트너 계정이라면, 해당하는 파트너의 실무자 리스트를 불러올 수 있도록 구현하였습니다. 가입 대기자의 경우도 동일한 방법을 통해 구현하였습니다.



## 📑 Info App

### 💻 개발 과정

#### 본인 인증 링크 생성

> 본인 인증 링크를 생성하는 api

client에서 요청을 보낼 때 Link 정보와 Customer 정보를 동시에 보내주기 때문에 Link 생성과 Customer 생성을 동시에 진행했어야 했습니다.

이를 구현하기 위해서 `LinkDetailSerializer`에 customers 속성을 추가하고 `create`를 override했습니다. `create` 혹은 `update` 메서드는 Serializer가 save될 때 작동하는 메서드입니다. 링크를 수정하는 일은 없으므로 `create`만 override하였습니다. 

```python
def create(self, validated_data):
    customers_data = validated_data.pop('customers')
    managers = validated_data.pop('managers')
    link = Link.objects.create(**validated_data)
    link.managers.set(managers)
    for customer_data in customers_data:
        Customer.objects.create(link=link, **customer_data)
    return link
```

customers와 managers를 pop하여 따로 저장한 다음에 Link object를 생성하였습니다. managers는 ManyToManyField이므로 .set을 이용하여 저장하였습니다. 그 후 customer object를 for문으로 돌면서 하나씩 생성하였습니다.



#### 본인 인증 링크 목록 조회

> 로그인한 유저가 관리하는 링크 목록을 조회하는 api

##### 문제1

이 기능을 개발하기 위해서 Link 테이블의 `managers` 필드에 로그인한 유저의 id값을 가지고 있는 Link 객체들을 가져와야 했습니다.

이를 위해 Django QuerySet API의 `filter`와 Field lookup의 `in`을 사용했습니다.

```django
Entry.objects.filter(id__in=[1, 3, 4])
```

위의 코드는 `id in [1, 3, 4]`의 값이 참인 objects를 포함하는 queryset을 반환하는데 문제는 `managers` 필드가 `ManyToManyField`로 되어있어서 `managers`값이 iterable한 객체였기 때문에 원하는 값이 나오지 않을 것이라고 생각했지만 제 생각과는 다르게 올바른 결과가 나왔습니다.

```
Link.objects.filter(managers__in=[user], expired_at__gt=timezone.now())
```

찾아보니 `ManyToManyField`, `ManyToOneField`의 경우에는 `user in managers`가 참인 objects를 포함하는 queryset을 반환하는 것으로 확인이 되었습니다. 위의 경우에는 `id` lookup을 이용할 수도 있습니다.

```
Link.objects.filter(managers__id=user.pk, expired_at__gt=timezone.now())
```

##### 문제2

링크 목록을 반환할 때 Link 테이블에 없는 Link와 관련된 customers의 수와 인증을 마친 customers의 수를 반환해줘야 했습니다.

이를 위해서 `LinkListSerializer`에 `SerializerMethodField`로 `total`, `complete_cnt` 두 개의 필드를 만들었고 값을 가져오기 위해 `get_total`, `get_complete_cnt` 메서드를 만들었습니다. `SerializerMethodField`는 `get_<field name>`이라는 메서드를 통해 값을 가져오기 때문입니다.



#### 신분증 OCR 및 비식별화





#### 고객 정보 저장





#### Permission class 커스터마이징

유저 모델에 approval 속성이 추가되면서 승인된 유저인지 아닌지 판별하는 로직을 뷰함수마다 추가하였습니다. 그러나 이 방법이 너무 비효율적인 것 같아서 다른 방법을 생각해보다 permission class를 만들어 사용하게 되었습니다.

permission class를 생성하는 과정이 복잡할 것 같았는데 굉장히 간단하게 생성할 수 있어서 역시 Django구나라는 생각이 들었습니다. 공식문서도 너무 잘 되어있어서 코드를 작성하는 데에는 많은 시간이 들지는 않았던 것 같습니다. 

수정 후 코드가 매우 깔끔해진 것을 보고 좋은 코드를 작성했다는 생각에 매우 뿌듯해했던 기억이 남습니다.



## 📑 배포 및 유지보수

- AWS 우분투 서버를 이용한 배포
- Frontend는 Nginx, Backend는 Gunicorn WSGI server 사용
- 보안 연결(HTTPS)은 certbot 이용 (https://certbot.eff.org/)
- DB는 Django 내장 DB인 sqlite3 이용
- 다양한 실제 테스트 데이터 삽입
- 각종 에러 & 이슈 사항 보완



## 📑 총평

- 권기웅 : 
- 이경민 : Django rest framework을 이용한 백엔드 개발과, aws ubuntu 환경에서의 배포 둘 다 처음 해 본 경험이었고 많은 시행착오를 겪게 되었습니다. 특히 기억에 남는 것은 ubuntu 환경은 권한에 매우 민감하다는 점이었습니다. 배포용 계정인 deploy를 생성하였다가, 서버쪽에서 수정이 필요할 때 마다 경로 및 파일의 권한을 바꿔야 하는 결과를 초래하였습니다. 또한 GUI가 아닌 터미널 환경에서 주로 작업하다 보니 처음에는 불편했지만 적응되고 나니 편리한 점도 많다고 느꼈습니다. 손이 키보드에서 마우스로 오갈 필요가 적은 점도 그렇고, 명령어에 익숙해지니 작업 속도가 빨라졌습니다. 세세한 부분까지 신경써야 하는 점이 개발자의 중요한 역량 중 하나라는 것을 느꼈습니다.

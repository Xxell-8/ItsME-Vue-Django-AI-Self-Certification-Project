# SERVER



## Accounts App



## Info App

### 기능

#### 본인 인증 링크 생성

> 본인 인증 링크를 생성하는 api





#### 본인 인증 링크 목록 조회

> 로그인한 유저가 관리하는 링크 목록을 조회하는 api

##### 문제1

이 기능을 개발하기 위해서 Link 테이블의 `managers` 필드에 로그인한 유저의 id값을 가지고 있는 Link 객체들을 가져와야 했습니다.

이를 위해 Django QuerySet API의 `filter`와 Field lookup의 `in`을 사용했습니다.

```django
Entry.objects.filter(id__in=[1, 3, 4])
```

위의 코드는 `id in [1, 3, 4]`의 값이 참인 objects를 포함하는 queryset을 반환하는데 문제는 `managers` 필드가 `ManyToManyField`로 되어있어서

`managers`값이 iterable한 객체였기 때문에 원하는 값이 나오지 않을 것이라고 생각했지만 제 생각과는 다르게 올바른 결과가 나왔습니다.

```
Link.objects.filter(managers__in=[user], expired_at__gt=timezone.now())
```

찾아보니 `ManyToManyField`, `ManyToOneField`의 경우에는 `user in managers`가 참인 objects를 포함하는 queryset을 반환하는 것으로 확인이 되었습니다. 위의 경우에는 `id` lookup을 이용할 수도 있습니다.

```
Link.objects.filter(managers__id=user.pk, expired_at__gt=timezone.now())
```

##### 문제2

링크 목록을 반환할 때 Link 테이블에 없는 Link와 관련된 customers의 수와 인증을 마친 customers의 수를 반환해줘야 했습니다.

이를 위해서 `LinkListSerializer`에 `SerializerMethodField`로 `total`, `complete_cnt` 두 개의 필드를 만들었고 `get_total`, `get_complete_cnt` 메서드를 만들어 원하는 값을 가져오게 하였습니다.



#### 본인 인증 링크 상세 조회



#### 본인 인증 링크 삭제



#### 신분증 OCR 및 비식별화



#### 고객 정보 저장



#### 파트너 기업의 링크 개수 조회




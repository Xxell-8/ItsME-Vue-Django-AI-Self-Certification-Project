# SERVER



## Accounts App



## Info App

### 개발 과정

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

> 고객의 신분증 사진에서 이름과 생일을 인식
>
> 신분증 이미지에서 개인정보를 마스킹
>
> 얼굴 사진과 신분증의 얼굴사진의 유사도를 측정하여 동일인물인지 판별

이 api를 위해 구현해야 하는 기능을 크게 나누어 보면 Text detection, Text recognition, image masking, compare face 네가지였습니다.

Text detection은 OpenCV를 활용하여 구현하였습니다. 이미지 

우선 신분증 OCR 기능을 구현하기 위해서 인공지능 모델을 직접 학습시기는 것과 tesseract-ocr 오픈소스를 활용하는 것 두가지 방법이 있었는데 저희는 tesseract-ocr을 사용하기로 정하였습니다. 한글 OCR 인공지능 모델을 학습시키는 데에 시간이 오래 걸릴 뿐만 아니라 성능에 대한 확신이 부족했기 때문입니다. 



#### Permission class 커스터마이징

유저 모델에 approval 속성이 추가되면서 승인된 유저인지 아닌지 판별하는 로직을 뷰함수마다 추가하였습니다. 그러나 이 방법이 너무 비효율적인 것 같아서 다른 방법을 생각해보다 permission class를 만들어 사용하게 되었습니다.

permission class를 생성하는 과정이 복잡할 것 같았는데 굉장히 간단하게 생성할 수 있어서 역시 Django구나라는 생각이 들었습니다. 공식문서도 너무 잘 되어있어서 코드를 작성하는 데에는 많은 시간이 들지는 않았던 것 같습니다. 

수정 후 코드가 매우 깔끔해진 것을 보고 좋은 코드를 작성했다는 생각에 매우 뿌듯해했던 기억이 남습니다.

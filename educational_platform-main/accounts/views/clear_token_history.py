from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import json
from accounts.models import TokenPurchase, UserToken

@login_required
@csrf_exempt
def purchase_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        price = data.get('price')

        # Создаем запись о покупке
        TokenPurchase.objects.create(
            user=request.user,
            amount=amount,
            price=price
        )

        # Обновляем баланс пользователя
        user_token, created = UserToken.objects.get_or_create(user=request.user)
        user_token.balance += Decimal(amount)  # Преобразуем amount в Decimal
        user_token.save()

        return JsonResponse({'status': 'success', 'new_balance': user_token.balance})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_exempt
def clear_history(request):
    if request.method == 'POST':
        TokenPurchase.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_token_balance(request):
    user_token, created = UserToken.objects.get_or_create(user=request.user)
    return JsonResponse({'balance': user_token.balance})

@login_required
def get_purchase_history(request):
    purchases = TokenPurchase.objects.filter(user=request.user).order_by('-purchased_at')
    history = [
        {
            'amount': purchase.amount,
            U'price': purchase.price,
            'date': purchase.purchased_at.isoformat()
        }
        for purchase in purchases
    ]
    return JsonResponse(history, safe=False)  # safe=False для списка
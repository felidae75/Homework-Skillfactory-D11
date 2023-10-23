from django import template

register = template.Library()


# Я не знаю, как это сделать без циклов. По максимуму их сократила
@register.filter(name='censor')
def censor(text):
    censored_words = ['fuck', 'shit', 'motherfucker', 'big']
    # Список плохих слов
    symbols_to_remove = """!?.-)(;:+=','"""
    for symbol in symbols_to_remove:
        text_no_spots = text.replace(symbol, " ")
    words_in_text = set(text_no_spots.lower().split())
    # Превращаем текст в множество, чтобы убрать повторы. Так быстрее искать

    for word in censored_words:
        if word in words_in_text:
            text = text.replace(word.title(), '(censored)')
            text = text.replace(word, '(censored)')
            text = text.replace(word.upper(), '(censored)')
    return text

# text = 'Fuck or fuck, or fuck! and something cat cat Cat.jpg !'
# symbols_to_remove = """!?.-)(;:+=','"""
# for symbol in symbols_to_remove:
#     text1 = text.replace(symbol, " ")
# censored_words = ['fuck', 'shit', 'motherfucker', 'cat']
# words_in_text = list(set(text1.lower().split()))
#
# for word in censored_words:
#     if word in words_in_text:
#         text = text.replace(word, '(censored)')
#         text = text.replace(word.upper(), '(censored)')
#         text = text.replace(word.title(), '(censored)')
# print(text)








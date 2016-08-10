__author__ = 'kirill'

token="207939931:AAGDd6FjCOQ07NNXs4KByV8zNYGJLttYC08"




digits_pattern=re.compile(r'[0-9]+ [0-9]+$',re.MULTILINE)


@bot.inline_handler(lambda query:len(query.query)>0)
def query_text(query):
    try:
        matches=re.match(digits_pattern,query.query)
    except AttributeError as ex:
        return

    num1,num2=matches.group().split()
    try:
        m_sum=int(num1)+int(num2)
        r_sum=types.InlineQueryResultArticle(
            id='1',
            parse_mode='Markdown',
            title='Sum',
            description='Result is: {!s}'.format(m_sum),
            message_text="{!s} + {!s}= {!s}".format(num1,num2,m_sum),
        )
        m_sub=int(num1)-int(num2)
        r_sub=types.InlineQueryResultArticle(id='2',title='Substination',
                                             description='Result is {!s}'.format(m_sum),
                                             input_message_context='{!s}-{!s}={!s}'.format(num1,num2,m_sum),
                                             )
        if num2 is not '0':
            m_div=int(num1)/int(num2)
            r_div=types.InlineQueryResultArticle(id='3',title='Division',
                                                 description='Result is {0:.2f}'.format(m_div),
                                                 input_message_context='{0!s}/{1!s}={2:.2f}'.format(num1,num2,m_div),
                                                 )
        else:
            r_div=types.InlineQueryResultArticle(id='3',title='Division',description="I cannot perform it!",
                                                 input_message_context='I am a good bot and dont perform division at zero'
                                                 )
        m_mul=int(num1)*int(num2)
        r_mul=types.InlineQueryResultArticle(
            id='4',title='Multiplication',
            description='Result is {!s}'.format(m_mul),
            input_message_context='{!s} *{!s} ={!s}'.format(num1,num2,m_mul),
        )
        bot.answer_inline_query(query.id,[r_sum,r_sub,r_div,r_mul])
    except Exception as e:
        print("{!s}\n{!s}".format(type(e),str(e)))


if __name__=='__main__':
    bot.polling(none_stop=True)
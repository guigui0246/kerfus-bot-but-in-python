def run(msg, client=None):
    "If 19:37 then polish song"
    import datetime
    date = datetime.datetime.now()
    if date.hour == 19 and date.minute == 37 and not msg.guild == 1121125014096318615 :
        msg.reply("""Pan kiedyś stanął nad brzegiem,\n
Szukał ludzi gotowych pójść za Nim;\n
By łowić serca\nSłów Bożych prawdą.\n
Ref.: O Panie, to Ty na mnie spojrzałeś,\n
Twoje usta dziś wyrzekły me imię.\n
Swoją barkę pozostawiam na brzegu,\n
Razem z Tobą nowy zacznę dziś łów.\n
2. Jestem ubogim człowiekiem,\n
Moim skarbem są ręce gotowe\n
Do pracy z Tobą\n
I czyste serce.\n
Ref.: O Panie, to Ty na mnie spojrzałeś,\n
Twoje usta dziś wyrzekły me imię.\n
Swoją barkę pozostawiam na brzegu,\n
Razem z Tobą nowy zacznę dziś łów.\n
3. Ty, potrzebujesz mych dłoni,\n
Mego serca młodego zapałem\n
Mych kropli potu\n
I samotności.\n
Ref.: O Panie, to Ty na mnie spojrzałeś,\n
Twoje usta dziś wyrzekły me imię.\n
Swoją barkę pozostawiam na brzegu,\n
Razem z Tobą nowy zacznę dziś łów.\n
4. Dziś wypłyniemy już razem\n
Łowić serca na morzach dusz ludzkich\n
Twej prawdy siecią\nI słowem życia.\n
Ref.: O Panie, to Ty na mnie spojrzałeś,\n
Twoje usta dziś wyrzekły me imię.\n
Swoją barkę pozostawiam na brzegu,\n
Razem z Tobą nowy zacznę dziś łów""")

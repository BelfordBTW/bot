import vk_api, sys, json
from vk_api.longpoll import VkLongPoll, VkEventType
from hidden_token import TOKEN

global_vk_session = vk_api.VkApi(token=TOKEN)
global_session_api = global_vk_session.get_api()
global_longpool = VkLongPoll(global_vk_session)


def main(vk_session, session_api, longpool, ):

    def get_username(uid):
        username = session_api.users.get(user_id=uid)
        return f"{username[0].get('first_name')} {username[0].get('last_name')}"

    def write_auditores(content):
        with open("auditores.json", "w") as w_aud:
            json.dump(content, w_aud)

    def big_clear(cab):
        for k in cab.keys():
            cab[k] = [0, 0, 0]

        write_auditores(cab)
        text = 'чисто'
        return text

    def read_auditores():
        with open("auditores.json", "r") as aud:
            return json.load(aud)

    def output(vks, uid, text, ):
        vks.method("messages.send", {"user_id": uid, "message": text, "random_id": 0})

    def get_take(cabs, raw_msg, uid):

        def take_attempt(try_username, try_cab_for_take, index):
            user_target = cabs[try_cab_for_take][index]
            if user_target == 0:
                cabs[try_cab_for_take][index] = try_username
                write_auditores(cabs)
                out = f'{try_username}, Вы успешно заняли аудиторию'
            else:
                out = f'Занято пользователем с именем {user_target}'

            return out

        text = 'Имя аудитории или номер пары incorrect'
        try:
            junk, cab_for_take, para = raw_msg.split(' ')

            if cab_for_take in cabs.keys() and int(int(para) - 1) in range(0, len(cabs.get(cab_for_take))):
                text = take_attempt(get_username(uid), cab_for_take, (int(para) - 1))

        except ValueError:
            text = 'Не понял ( ͡° ͜ʖ ͡°) \n take [аудитория] [номер пары]'

        return text

    def get_free(cabs):

        text = "На данный момент все удитории заняты   (つ . •́ _ʖ •̀ .)つ "
        free_cabs = []
        isnot_free = True

        for cab in cabs.keys():
            free_time = []
            if 0 in cabs[cab]:
                isnot_free = False
                for index, para in enumerate(cabs[cab]):
                    if para == 0:
                        free_time.append(f'{index + 1}-я пара')
                free_cabs.append(f'{cab} : {", ".join(free_time)}')
            elif isnot_free:
                return text
            text = ("Список свободных аудиторий: \n\n\n" + " \n".join(free_cabs))

        return text

    def get_response(lp, vks):

        for event in lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                uid = event.user_id
                text_for_sender = "Я не понял ( ͡° ͜ʖ ͡°) \n\n\n\n all - Полный список\n free - Список свободных \n take [аудитория] [номер пары] - Занять аудиторию \n clear - чистить"

                if '404' in msg:
                    text_for_sender = 'NOT FOUND (ノ°益°)ノ'
                elif msg == "all":
                    all_cab = (" \n".join(read_auditores()))
                    text_for_sender = ("Полный список аудиторий: \n\n\n" + all_cab)
                elif msg == "free":
                    text_for_sender = get_free(read_auditores())
                elif 'take' in msg:
                    text_for_sender = get_take(read_auditores(), msg, uid)
                elif 'clear' in msg:
                    text_for_sender = big_clear(read_auditores())

                output(vks, uid, text_for_sender)

    get_response(longpool, vk_session)


if __name__ == "__main__":
    main(global_vk_session, global_session_api, global_longpool, )
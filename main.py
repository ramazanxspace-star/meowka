import telebot
from telebot import types
import time
import random
from datetime import datetime

# Токен вашего бота
TOKEN = '8296036510:AAH1cWHHPeoUlu4I3eZxnXNOtVW4ipNKElA'
bot = telebot.TeleBot(TOKEN)

# Хранилище для сообщений с маникенами (chat_id -> list of message_ids)
active_manikins = {}
# Флаг для тишины (per chat)
territory_silence = {}
# Счетчик маникенов
manikin_counter = {}

# Списки разнообразных текстов для изюминки
MANIKIN_MESSAGES = [
    "Маникен вышел из древесного дворца и готов яростно сражаться до смерти",
    "Маникен выполз из щели в полу, его стеклянные глаза горят мрачным огнём 🔥",
    "Маникен материализовался из тени, его деревянные суставы скрипят в предвкушении битвы",
    "Маникен спустился с балки, в его пустом взгляде читается древняя ярость",
    "Маникен возник из ниоткуда, шепча проклятия на забытом языке",
    "Маникен вылез из старого шкафа, пахнущего ладаном и пылью веков",
    "Маникен пробудился от векового сна, его пальцы сжимают невидимое оружие",
    "Маникен просочился сквозь стену, оставляя за собой след древесной стружки",
    "Маникен восстал из груды старых вещей, его движения неестественно резки",
    "Маникен появился в клубах странного тумана, его силуэт мерцает в полутьме"
]

MANIKIN_EMOJIS = ["🧸", "🪵", "🎭", "👤", "🗿", "🪆", "👹", "💀", "👻", "🎪"]

SILENCE_MESSAGES = [
    "Территория расширена, гробовая тишина пугает маникенов...",
    "Протяжный звон колоколов оповестил о расширении границ. Тишина стала зловещей... 🔔",
    "Воздух застыл. Звуки замерли. Территория охвачена кладбищенской тишиной... ⚰️",
    "Тишина опустилась как саван. Даже ветер не смеет шелохнуться... 🕯️",
    "Границы раздвинулись. Теперь здесь правит безмолвие, нарушаемое лишь шепотом ушедших... 👻",
    "Территория поглощена тишиной такой густой, что её можно резать ножом... 🔪",
    "Кладбищенская тишина окутала всё вокруг. Маникены замерли в ожидании... ⚱️"
]

GLAS_MESSAGES = [
    "Глас ударил по всей территории тишины",
    "СВЕРХЗВУКОВОЙ ГЛАС РАЗОРВАЛ ТИШИНУ! Волна звука сметает всё на своём пути!!! 🔊💥",
    "Громоподобный крик эхом пронзил безмолвие, заставляя вибрировать саму материю! 🌪️",
    "Глас, рождённый в недрах ада, пронёсся по территории, не оставляя шансов маникенам! 👹🔥",
    "Звуковая волна, способная разорвать душу, обрушилась на безмолвные земли! 💢⚡",
    "Рев, от которого трескаются камни и гнутся металлы, выкосил ряды маникенов! 🏹💣",
    "Сверхзвуковой рёв разорвал ткань реальности, уничтожая всё в радиусе поражения! 🌌💫"
]

BLOOD_EMOJIS_SEQUENCES = [
    ["🩸", "💀", "☠️", "🩸", "💥", "🩸"],
    ["🩸🔥", "💀⚡", "☠️💥", "💀🔥", "☠️⚡", "💀💥"],
    ["💥", "💢", "💀", "☠️", "🩸", "🔥"],
    ["🩸🩸🩸", "💀💀💀", "☠️☠️☠️", "🔥🔥🔥", "💥💥💥", "⚰️⚰️⚰️"]
]

DESTRUCTION_MESSAGES = [
    "Все маникены уничтожены...",
    "Последние щепки маникенов унесены ветром... Их больше нет. 🍃",
    "Там, где секунду назад стояли маникены, теперь лишь пыль и тишина... 🏚️",
    "От маникенов не осталось и следа. Лишь лёгкий запах гари и старое дерево... 🌫️",
    "Маникены обращены в пепел. Территория очищена. ✅",
    "Великая чистка завершена. Ни один маникен не устоял перед гласом... 🧹",
    "Армия маникенов повержена! Поле битвы пусто... 🏆"
]

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    welcome_text = """🎪 *Добро пожаловать в Цирк Древесных Маникенов!* 🎪

*Доступные команды:*

🤖 *Выпустить (число) живых маникенов*
_Выпускает армию маникенов для битвы_

⚰️ *Расширение территории кладбищенская тишина*
_Расширяет границы и наводит ужасную тишину_

🔊 *Сверхзвуковой глас*
_Уничтожает всех маникенов звуковой волной (только после активации тишины)_

📊 *Статистика*
_Показывает ваши достижения_

🪵 *Инфо*
_Информация о маникенах_

_Используйте команды как есть или с маленькой буквы_"""
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['статистика', 'stats'])
def stats_command(message):
    chat_id = message.chat.id
    total_created = manikin_counter.get(chat_id, 0)
    
    stats_text = f"""📊 *Ваша статистика маникенов:*

🎪 Всего выпущено: *{total_created}* маникенов
💀 Уничтожено за всё время: *{total_created}* маникенов
⚔️ Битв проведено: *{len(active_manikins.get(chat_id, [])) if chat_id in active_manikins else 0}*
👑 Ранг: *{get_rank(total_created)}*

_Продолжайте в том же духе! Маникены ждут своей участи..._"""
    
    bot.send_message(chat_id, stats_text, parse_mode='Markdown')

@bot.message_handler(commands=['инфо', 'info'])
def info_command(message):
    info_text = """🪵 *Информация о Древесных Маникенах:*

*Происхождение:* Маникены выходят из Древесного Дворца - таинственного места между мирами.

*Способности:*
• Неутомимость в бою
• Деревянная непробиваемость
• Вечная готовность сражаться

*Слабости:*
• Кладбищенская тишина
• Сверхзвуковой глас
• Сильный огонь

*Предупреждение:* Не выпускайте слишком много маникенов одновременно!"""
    
    bot.send_message(message.chat.id, info_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.lower()
    chat_id = message.chat.id
    
    # Команда выпуска маникенов
    if text.startswith('выпустить'):
        try:
            parts = message.text.split()
            count = int(parts[1])
            
            if count <= 0:
                bot.send_message(chat_id, "❌ Нельзя выпустить отрицательное или нулевое количество маникенов!")
                return
                
            if count > 50:
                count = 50
                warning_msg = random.choice([
                    "⚠️ Ты что, хочешь устроить апокалипсис? Выпускаю 50 маникенов!",
                    "⚠️ Слишком много! Придется ограничиться 50 маникенами.",
                    "⚠️ Армия не может быть бесконечной! 50 маникенов - это максимум."
                ])
                bot.send_message(chat_id, warning_msg)
            
            # Обновляем счетчик
            manikin_counter[chat_id] = manikin_counter.get(chat_id, 0) + count
            
            # Отправляем предупреждение для большого количества
            if count > 20:
                bot.send_message(chat_id, f"🚨 *ВНИМАНИЕ!* Выпускаю {count} маникенов! Приготовьтесь!", parse_mode='Markdown')
                time.sleep(1)
            
            send_manikins(chat_id, count)
            
        except (IndexError, ValueError):
            bot.send_message(chat_id, "❌ *Использование:* Выпустить (число) живых маникенов\n_Пример: Выпустить 5 живых маникенов_", parse_mode='Markdown')
    
    # Команда расширения территории
    elif 'расширение территории кладбищенская тишина' in text:
        if territory_silence.get(chat_id, False):
            bot.send_message(chat_id, "⚠️ Тишина уже установлена! Территория и так замерла в ожидании...")
            return

        territory_silence[chat_id] = True
        message_text = random.choice(SILENCE_MESSAGES)
        
        # Добавляем эффект с задержкой
        msg = bot.send_message(chat_id, "🌫️ Тишина начинает опускаться...")
        time.sleep(1)
        bot.edit_message_text("🌫️🌫️ Тишина сгущается...", chat_id, msg.message_id)
        time.sleep(1)
        bot.edit_message_text(message_text, chat_id, msg.message_id)
        
        # Если есть активные маникены, добавляем эффект тишины
        if chat_id in active_manikins and active_manikins[chat_id]:
            time.sleep(0.5)
            bot.send_message(chat_id, "🤫 Маникены замерли в страхе...")

            # Замораживаем сообщения маникенов эффектом тишины
            silence_emojis = ["❄️", "🧊", "🌫️", "⚰️", "👻"]
            for i, msg_id in enumerate(active_manikins[chat_id]):
                try:
                    silence_emoji = silence_emojis[i % len(silence_emojis)]
                    bot.edit_message_text(f"{silence_emoji} Маникен замёрз в тишине... {silence_emoji}", chat_id, msg_id)
                    time.sleep(0.1)
                except Exception as e:
                    pass
    
    # Команда сверхзвукового гласа
    elif 'сверхзвуковой глас' in text:
        if not territory_silence.get(chat_id, False):
            bot.send_message(chat_id, "❌ *Сначала нужно расширить территорию!*\n_Используйте: Расширение территории кладбищенская тишина_", parse_mode='Markdown')
            return

        if chat_id not in active_manikins or not active_manikins[chat_id]:
            bot.send_message(chat_id, "🤷 На территории нет маникенов для уничтожения...")
            territory_silence[chat_id] = False
            return
        
        message_text = random.choice(GLAS_MESSAGES)
        bot.send_message(chat_id, f"🔊 *{message_text}*", parse_mode='Markdown')
        
        # Эффект нарастания звука
        time.sleep(0.5)
        bot.send_message(chat_id, "💢 ЗВУКОВАЯ ВОЛНА НАРАСТАЕТ...")
        time.sleep(0.3)
        
        destroy_all_manikins(chat_id)
        
    # Ответ на приветствия
    elif any(word in text for word in ['привет', 'hello', 'hi', 'здравствуй']):
        greetings = ["Приветствую в Цирке Маникенов! 🎪", "Здравствуй, повелитель маникенов! 👑", "Привет! Готов выпустить маникенов? 🤖"]
        bot.send_message(chat_id, random.choice(greetings))

def send_manikins(chat_id, count):
    """Отправляет указанное количество сообщений с маникенами"""
    if chat_id not in active_manikins:
        active_manikins[chat_id] = []
    
    # Предварительное сообщение
    if count > 10:
        bot.send_message(chat_id, f"🎪 *Начинаю выпуск {count} маникенов!*", parse_mode='Markdown')
    
    for i in range(count):
        # Случайный выбор сообщения и эмодзи
        message = random.choice(MANIKIN_MESSAGES)
        emoji = random.choice(MANIKIN_EMOJIS)
        
        # Добавляем номер маникена для больших количеств
        if count > 5:
            message = f"{emoji} Маникен #{i+1}: {message}"
        else:
            message = f"{emoji} {message}"
        
        # Для каждого 10-го маникена добавляем особый эффект
        if (i + 1) % 10 == 0 and i > 0:
            message += f"\n⭐ *ОСОБЫЙ МАНИКЕН!* Сильнее и опаснее! ⭐"
            msg = bot.send_message(chat_id, message, parse_mode='Markdown')
        else:
            msg = bot.send_message(chat_id, message)
        
        active_manikins[chat_id].append(msg.message_id)
        
        # Разная задержка в зависимости от количества
        delay = max(0.05, 0.3 - (count * 0.005))
        time.sleep(delay)
    
    # Финальное сообщение
    if count >= 10:
        endings = [
            f"🎪 *Армия из {count} маникенов готова к бою!*",
            f"⚔️ {count} маникенов выстроились в боевой порядок!",
            f"👹 Орда маникенов жаждет битвы! Всего: {count} воинов!"
        ]
        bot.send_message(chat_id, random.choice(endings), parse_mode='Markdown')

def destroy_all_manikins(chat_id):
    """Уничтожает все маникены с анимацией"""
    total_manikins = len(active_manikins[chat_id])

    # Эффект уничтожения
    for i, msg_id in enumerate(active_manikins[chat_id]):
        try:
            blood_sequence = random.choice(BLOOD_EMOJIS_SEQUENCES)

            # Для каждого маникена своя анимация
            for j, emoji in enumerate(blood_sequence):
                # Добавляем прогресс для больших количеств
                progress = f" [{i+1}/{total_manikins}]" if total_manikins > 5 else ""
                destruction_text = f"{emoji} Маникен уничтожается{progress}"

                # Для каждого 5-го кадра добавляем звуковой эффект
                if j % 5 == 0:
                    destruction_text += " 🔊"

                bot.edit_message_text(destruction_text, chat_id, msg_id)
                time.sleep(0.2)

        except Exception as e:
            # Сообщение могло быть удалено или недоступно
            pass

    # Финальная анимация
    time.sleep(0.5)
    final_msg = bot.send_message(chat_id, "💥 *ФИНАЛЬНЫЙ ВЗРЫВ!* 💥", parse_mode='Markdown')
    time.sleep(0.7)
    bot.edit_message_text("💥 *ФИНАЛЬНЫЙ ВЗРЫВ!* 💥\n🔥🔥🔥", chat_id, final_msg.message_id)

    # Удаляем все сообщения
    time.sleep(1)
    for msg_id in active_manikins[chat_id]:
        try:
            bot.delete_message(chat_id, msg_id)
        except:
            pass

    # Удаляем финальное сообщение
    try:
        bot.delete_message(chat_id, final_msg.message_id)
    except:
        pass

    # Очищаем список
    active_manikins[chat_id] = []
    territory_silence[chat_id] = False
    
    # Финальное сообщение с изюминкой
    destruction_message = random.choice(DESTRUCTION_MESSAGES)
    stats_message = f"\n\n📊 *Итог битвы:*\n🎪 Выпущено: {total_manikins} маникенов\n💀 Уничтожено: {total_manikins} маникенов\n🏆 Эффективность: 100%"
    
    bot.send_message(chat_id, f"{destruction_message}{stats_message}", parse_mode='Markdown')

def get_rank(total_manikins):
    """Определяет ранг пользователя по количеству выпущенных маникенов"""
    if total_manikens == 0:
        return "Новичок 🐣"
    elif total_manikens < 10:
        return "Ученик маникеноведа 📚"
    elif total_manikens < 50:
        return "Повелитель маникенов 👑"
    elif total_manikens < 100:
        return "Мастер древесных воинов 🪓"
    elif total_manikens < 500:
        return "Легенда цирка маникенов 🎪"
    else:
        return "БОГ МАНИКЕНОВ 🌟"

# Запуск бота
if __name__ == '__main__':
    print("🎪 Цирк Древесных Маникенов открыт!")
    print("🤖 Бот запущен и готов к работе...")
    print("=" * 40)
    bot.polling(none_stop=True)

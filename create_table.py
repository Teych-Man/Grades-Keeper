import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#! ----------------------------------------------------------------------------------------------------------------

mouth = {
    "Январь": 31,
    "Февраль": 28,
    "Март": 31,
    "Апрель": 30,
    "Май": 31,
    "Июнь": 30,
    "Июль": 31,
    "Август": 31,
    "Сентябрь": 30,
    "Октябрь": 31,
    "Ноябрь": 30,
    "Декабрь": 31
}

#! ----------------------------------------------------------------------------------------------------------------

async def create_table_from_excel(select_name, mounth_sender, path_to_excel, message):
    day = mouth.get(mounth_sender, 31)
    
    df = pd.read_excel(path_to_excel)

    user_data = df[df.iloc[:, 0] == select_name].iloc[:, 1:day+1].values.flatten()

    data = np.empty((day + 2, 2), dtype=object)  
    data[0, 0] = "Число"
    data[0, 1] = "Баллы"

    for i in range(1, day + 1):
        data[i, 0] = i

    for i in range(1, len(user_data) + 1):
        if not pd.isna(user_data[i - 1]):
            data[i, 1] = round(user_data[i - 1])  
        else:
            data[i, 1] = "Нет оценки"

    valid_scores = [round(score) for score in user_data if not pd.isna(score)]
    average_score = round(np.mean(valid_scores)) if valid_scores else "Нет оценки"

    data[day + 1, 0] = "Средний балл"
    data[day + 1, 1] = average_score

    fig, ax = plt.subplots()
    ax.axis('off')

    table = ax.table(cellText=data, loc='center', cellLoc='center')

    for i in range(1, day + 2):  
        score = user_data[i - 1] if i <= day else average_score
        
        if pd.isna(score):
            text_color = 'black'  
        elif score == "Нет оценки":
            text_color = 'black'  
        elif score <= 49:
            text_color = 'red'
        elif 50 <= score <= 69:
            text_color = 'orange'
        elif 70 <= score <= 89:
            text_color = 'green'
        elif 90 <= score <= 100:
            text_color = 'darkgreen'
        
        table[i, 1].set_text_props(color=text_color)  

    for j in range(2):
        table[0, j].set_facecolor('grey')

    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor('black')

    path = fr'photo/{message.from_user.id}.png'
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()  

    return path
import streamlit as st
import pandas as pd
import json
import os
import shutil
from datetime import datetime

# JSON 파일 경로 설정
DATA_FILE = "apps_data.json"
BACKUP_DIR = "backup"  # 백업 저장 디렉터리 설정

# 백업 디렉터리가 없으면 만듭니다.
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# 앱 목록을 로드하는 함수
def load_app_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []  # 파일이 없으면 빈 리스트 반환

# 앱 데이터를 저장하는 함수
def save_app_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

# 앱 추가 함수 정의
def add_app(name, description, rating, comment, genre):
    # 중복 검사
    for app in st.session_state.app_list:
        if app['name'] == name:
            return False  # 이미 존재하는 앱이므로 False 반환
    # 앱 정보를 추가
    new_app = {
        "name": name,
        "description": description,
        "rating": rating,
        "comment": comment,
        "genre": genre
    }
    st.session_state.app_list.append(new_app)
    save_app_data(st.session_state.app_list)  # 데이터 저장
    return True

# 앱 삭제 함수 정의
def delete_app(name):
    st.session_state.app_list = [app for app in st.session_state.app_list if app['name'] != name]
    save_app_data(st.session_state.app_list)

# 앱 수정 함수 정의
def update_app(name, new_rating, new_genre):
    for app in st.session_state.app_list:
        if app["name"] == name:
            app["rating"] = new_rating
            app["genre"] = new_genre
            save_app_data(st.session_state.app_list)  # 데이터 저장
            break

# 앱 세부 정보를 보여주는 함수
def show_app_details(app):
    st.subheader(app['name'])
    st.write("설명: ", app['description'])
    st.write("평가: ", app['rating'])
    st.write("장르: ", app['genre'])
    st.write("댓글: ", app.get('comment', "없음"))
    st.write("---")

# 번역 데이터 설정
translations = {
    'ko': {
        'title': "내 앱 기록 및 평가 앱",
        'app_name': "앱 이름을 입력하세요:",
        'app_description': "앱 설명을 입력하세요:",
        'app_rating': "평가 (1-5 점)",
        'app_comment': "댓글을 입력하세요:",
        'select_genre': "장르를 선택하세요:",
        'add_app_button': "앱 추가",
        'delete_app': "삭제할 앱을 선택하세요",
        'delete_app_button': "앱 삭제",
        'update_app': "수정할 앱을 선택하세요",
        'update_rating': "새 평가 (1-5 점)",
        'update_genre': "새 장르를 선택하세요:",
        'update_app_button': "앱 수정",
        'saved_apps': "저장된 앱 목록",
        'no_apps': "저장된 앱이 없습니다.",
        'app_added': "'{app_name}' 앱이 추가되었습니다.",
        'app_exists': "'{app_name}' 앱은 이미 목록에 있습니다.",
        'app_deleted': "'{app_name}' 앱이 삭제되었습니다.",
        'app_updated': "'{app_name}' 앱의 평가와 장르가 수정되었습니다."
    },
    'en': {
        'title': "My App Recording and Evaluation App",
        'app_name': "Enter app name:",
        'app_description': "Enter app description:",
        'app_rating': "Rating (1-5)",
        'app_comment': "Enter comment:",
        'select_genre': "Select genre:",
        'add_app_button': "Add App",
        'delete_app': "Select app to delete",
        'delete_app_button': "Delete App",
        'update_app': "Select app to update",
        'update_rating': "New rating (1-5)",
        'update_genre': "Select new genre:",
        'update_app_button': "Update App",
        'saved_apps': "Saved App List",
        'no_apps': "No saved apps.",
        'app_added': "'{app_name}' app has been added.",
        'app_exists': "'{app_name}' app already exists in the list.",
        'app_deleted': "'{app_name}' app has been deleted.",
        'app_updated': "'{app_name}' app's rating and genre have been updated."
    }
}

# 앱 목록 로드
if 'app_list' not in st.session_state:
    st.session_state.app_list = load_app_data()

# 장르 목록 정의
genre_options = ["게임", "교육", "생산성", "소셜 미디어", "건강", "기타"]

# 언어 설정
if 'language' not in st.session_state:
    st.session_state.language = 'ko'  # 기본 언어를 한국어로 설정

# 사이드바 메뉴
st.sidebar.title("메뉴")
menu = st.sidebar.radio("선택하세요:", ["앱 추가", "앱 삭제", "앱 수정", "앱 목록 보기", "앱 선택"])

# 언어 선택 드롭다운
language = st.sidebar.selectbox("언어를 선택하세요:", options=["ko", "en"],
                                  format_func=lambda x: "한국어" if x == "ko" else "English")
st.session_state.language = language  # 선택한 언어 저장

# 앱 제목
st.title(translations[st.session_state.language]['title'])

if menu == "앱 추가":
    # 앱 추가 입력란
    app_name_input = st.text_input(translations[st.session_state.language]['app_name'])
    app_description_input = st.text_area(translations[st.session_state.language]['app_description'])
    rating_input = st.select_slider(translations[st.session_state.language]['app_rating'], options=[1, 2, 3, 4, 5])
    comment_input = st.text_area(translations[st.session_state.language]['app_comment'])
    genre_input = st.selectbox(translations[st.session_state.language]['select_genre'], genre_options)

    # 앱 추가 버튼
    if st.button(translations[st.session_state.language]['add_app_button']):
        if app_name_input and app_description_input:
            if add_app(app_name_input, app_description_input, rating_input, comment_input, genre_input):
                st.success(translations[st.session_state.language]['app_added'].format(app_name=app_name_input))
            else:
                st.warning(translations[st.session_state.language]['app_exists'].format(app_name=app_name_input))
        else:
            st.warning("앱 이름과 설명을 입력하세요.")

elif menu == "앱 삭제":
    # 앱 삭제 입력란
    app_name_delete = st.selectbox(translations[st.session_state.language]['delete_app'],
                                    [app["name"] for app in st.session_state.app_list])

    # 앱 삭제 버튼
    if st.button(translations[st.session_state.language]['delete_app_button']):
        if app_name_delete:
            delete_app(app_name_delete)
            st.success(translations[st.session_state.language]['app_deleted'].format(app_name=app_name_delete))
        else:
            st.warning("삭제할 앱을 선택하세요.")

elif menu == "앱 수정":
    # 앱 수정 입력란
    app_name_update = st.selectbox(translations[st.session_state.language]['update_app'],
                                    [app["name"] for app in st.session_state.app_list])
    new_rating_input = st.select_slider(translations[st.session_state.language]['update_rating'], options=[1, 2, 3, 4, 5])
    new_genre_input = st.selectbox(translations[st.session_state.language]['update_genre'], genre_options)

    # 앱 수정 버튼
    if st
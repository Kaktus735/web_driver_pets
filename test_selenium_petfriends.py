import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    # Авторизуемся

    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    yield

    pytest.driver.quit()


# Явные ожидания, проверка карточек питомцев
def test_web_driver_wait():
    # Неявное ожидание фото
    images = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-img-top'))
    )
    # Неявное ожидание имён
    names = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-body .card-title'))
    )
    # Неявное ожидание описания (породы и возраста)
    descriptions = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-body .card-text'))
    )

    # Src фотографий
    src_images = [x.get_attribute('src') for x in images]
    # Text имен
    text_names = [x.text for x in names]
    # Text возраста
    text_ages = [x.text.split(', ')[1] for x in descriptions]

    # Число найденных элементов одинаковое (небольшой смок тест,
    # что элементы получены, ожидания отработали)
    assert len(src_images) == len(text_names)
    assert len(src_images) == len(text_ages)


# Неявные ожидания, проверка таблицы питомцев
# Поскольку в задании явно не указано, к каким именно элементам необходимо
# добавить явные ожидания, выбраны те же элементы, что и с явными ожиданиями
def test_web_driver_implicitly_wait():
    # Устанавливаем неявное ожидание
    pytest.driver.implicitly_wait(10)

    # Переходим на страницу c таблицей питомцев
    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')

    images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/th[1]')
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[1]')
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[3]')

    # Src фотографий
    src_images = [x.get_attribute('src') for x in images]
    # Text имен
    text_names = [x.text for x in names]
    # Text возраста
    text_ages = [x.text for x in ages]

    # Число найденных элементов одинаковое (небольшой смок тест,
    # что элементы получены, ожидания отработали)
    assert len(src_images) == len(text_names)
    assert len(src_images) == len(text_ages)

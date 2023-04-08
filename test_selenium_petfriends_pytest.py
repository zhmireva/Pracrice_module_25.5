import time
import pytest
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True, scope="class")
def start_setup():
    # заходим на страницу /my_pets
    pytest.driver = webdriver.Chrome(r'C:\Users\Вяткины\PycharmProjects\practice_25_5/chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.maximize_window()
    pytest.driver.find_element(By.ID, 'email').send_keys('zhmireva@gmail.com')
    pytest.driver.find_element(By.ID, 'pass').send_keys('zhmir17071990')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    # получаем общее количество питомцев
    counting_pets = pytest.driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]').text
    still_counting_pets = counting_pets.split()
    pytest.pet_count = int(still_counting_pets[2])
    # убеждаемся что питомцев больше 0
    assert pytest.pet_count > 0

    yield

    pytest.driver.quit()


class TestsPf:
    def test_has_all_pets(self):
        pytest.driver.implicitly_wait(5)
        pets_on_page = len(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
        assert pets_on_page == pytest.pet_count

    def test_more_than_50_percent_photos(self):
        # получаем данные о фото питомоцев
        pytest.driver.implicitly_wait(5)
        photos = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
        # считаем количество питомцев с фото
        pets_with_photos = 0
        for i in range(pytest.pet_count):
            if photos[i].get_attribute('src') != '':
                pets_with_photos = pets_with_photos + 1
        # сравниваем
        assert pets_with_photos >= pytest.pet_count/2

    def test_all_pets_have_name_breed_age(self):
        # получаем данные об именах/породах/возрасте питомцев
        pytest.driver.implicitly_wait(5)
        names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
        pytest.driver.implicitly_wait(5)
        breeds = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
        pytest.driver.implicitly_wait(5)
        ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
        # проверяем везде ли есть данные
        for i in range(pytest.pet_count):
            assert names[i].text != ''
            assert breeds[i].text != ''
            assert ages[i].text != ''

    def test_all_names_are_different(self):
        # получаем данные об именах/породах/возрасте питомцев
        pytest.driver.implicitly_wait(5)
        names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
        names_array = []
        # Создаем массив с именами, добавляем в него все кроме пустых полей
        for i in range(pytest.pet_count):
            if names[i].text != '':
                names_array.append(names[i].text)
        # Сравниваем имена питомцев в массиве
        for i in range(pytest.pet_count):
            for j in range(i+1, pytest.pet_count):
                assert names_array[i] != names_array[j]

    def test_no_repeating_pets(self):
        # добавляем явное ожидание пока прогрузятся все карточки питомцев
        WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))
        # получаем данные об именах/породах/возрасте питомцев
        names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
        breeds = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
        ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
        # создаем массив с массивами данных каждого питомца, пустые поля игнорируем
        giga_array = []
        for i in range(pytest.pet_count):
            giga_array.append([names[i].text, breeds[i].text, ages[i].text])
        # сравниваем питомцев в массиве
        for i in range(pytest.pet_count):
            for j in range(i+1, pytest.pet_count):
                assert giga_array[i] != giga_array[j]

from bs4.element import *
from datetime import datetime, timedelta, date
import pandas as pd
import unidecode

def remove_accents_and_spaces(text):
    # Loại bỏ dấu
    text_without_accents = unidecode.unidecode(text)
    # Loại bỏ khoảng cách
    text_without_spaces = text_without_accents.replace(" ", "")
    return text_without_spaces

def date_arithmetics(start_date, durations, mode = 'addition'):
    parsed_start_date = datetime.strptime(start_date, "%d-%m-%Y")
    
    if mode.lower() == 'subtraction':
        pass
    elif mode.lower() == 'multiplication':
        pass
    elif mode.lower() == 'division':
        pass
    else:
        return (parsed_start_date + timedelta(days = durations)).strftime("%d-%m-%Y")

def get_hotel_geo_id_based_on_location(location):
    hotel_geo_data = pd.read_csv("C:/Projects/Python/DataScience/data/traveloka/traveloka hotel geo data.csv")
    return hotel_geo_data.set_index("location").loc[location]["hotel_geo_id"]

def check_input_date_in_one_year_ahead_range(today_date, check_in_date):
    one_year_ahead_date = today_date.replace(year = today_date.year + 1)

    if today_date <= check_in_date <= one_year_ahead_date:
        return True

    return False

def diff_month(today_date, check_in_date):
    diff_year = check_in_date.year - today_date.year

    if diff_year == 0:
        return check_in_date.month - today_date.month
    else:
        return 12 - today_date.month + check_in_date.month
    
def define_the_month_index_of_check_in_date_on_the_date_picker(check_in_date):
    today_date = date.today()
    
    if check_input_date_in_one_year_ahead_range(today_date, check_in_date):
        return diff_month(today_date, check_in_date) + 1
    else:
        raise Exception("")

def define_hotel_rating_and_reviewers(hotels):
    ratings = []
    reviewers = []
    for hotel in hotels:
        sibling = hotel.parent.find_next_sibling('div')
        if sibling == None:
            ratings.append(0)
            reviewers.append(0)
        else:
            rating_and_reviewers = sibling.find("div", class_ = "css-901oao r-a5wbuh r-1b43r93 r-b88u0q r-rjixqe r-fdjqy7").text
            ratings.append(define_rating(rating_and_reviewers))
            reviewers.append(define_reviewers(rating_and_reviewers))

    return ratings, reviewers

# def define_hotel_rating_and_reviewers(hotels):
#     ratings = []
#     reviewers = []
    
#     for hotel in hotels:
#         sibling = hotel.parent.find_next_sibling('div')
        
#         # Kiểm tra nếu sibling là None
#         if sibling is None:
#             print(f"Sibling not found for hotel: {hotel.text}")
#             ratings.append(0)
#             reviewers.append(0)
#         else:
#             # Tìm div chứa rating và reviewers
#             rating_div = sibling.find("div", class_="css-901oao r-t1w4ow r-1b43r93 r-b88u0q r-rjixqe r-fdjqy7")
            
#             # Kiểm tra nếu không tìm thấy rating_div
#             if rating_div is None:
#                 print(f"Rating div not found for hotel: {hotel.text}")
#                 ratings.append(0)
#                 reviewers.append(0)
#             else:
#                 # Nếu tìm thấy rating_div, lấy text
#                 rating_and_reviewers = rating_div.text
#                 ratings.append(define_rating(rating_and_reviewers))
#                 reviewers.append(define_reviewers(rating_and_reviewers))
    
#     return ratings, reviewers


def define_rating(rating_and_reviewers):
    return float(rating_and_reviewers[0:rating_and_reviewers.index("(")])

def define_reviewers(rating_and_reviewers):
    # Tách số lượng reviewers từ chuỗi bằng cách lấy phần giữa dấu ngoặc
    reviewers = rating_and_reviewers[rating_and_reviewers.index("(") + 1 : rating_and_reviewers.index(")")]

    # Kiểm tra và xử lý trường hợp số lượng reviews có định dạng khác
    if "reviews" not in reviewers:
        return int(reviewers)  # Trường hợp không có từ "reviews", trả về giá trị nguyên
    
    # Xử lý trường hợp có chữ "K" (ví dụ: "1.6K reviews")
    if "K" in reviewers:
        # Chuyển đổi thành float và nhân với 1000
        return int(float(reviewers[0:reviewers.index("K")].replace(",", ".")) * 1000)
    
    # Xử lý trường hợp bình thường khi không có "K"
    return int(float(reviewers[0:reviewers.index("reviews")].replace(",", ".")))


def reformat_price(prices):
    reformatted_prices = []
    for price in prices:
        temp_price = price.text
        temp_price = temp_price.replace("VND", "")
        temp_price = temp_price.replace(".", "")
        reformatted_prices.append(int(temp_price))
        
    return reformatted_prices




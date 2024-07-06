import pickle
import pandas as pd
from data_preset import data as preset_data
from warnings import simplefilter

# Can be ignored, only one row in the DataFrame
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Load the saved model
loaded_model = pickle.load(open("./models/pima.pickle.dat", "rb"))

def get_salary(form_data):
    # Extract the data from the form
    country = form_data.get('Land')
    industry = form_data.get('Branche')
    education = form_data.get('Bildungsabschluss')
    gender = form_data.get('Geschlecht')
    age = form_data.get('Alter')
    experience_overall = form_data.get('Erfahrung')
    experience_field = form_data.get('Erfahrung im Berufsfeld')

    prepared_data = prepare_data(
        country, industry, education, gender, age, experience_overall, experience_field)

    res = predict_salary(prepared_data)

    # Round to get rid of decimal places
    res = round(res)
    return res


def predict_salary(data):
    predictions = loaded_model.predict(data)
    return predictions[0]

# modelData = data[['country', 'industry', 'education_class', 'gender', 'age_class', 'exp_overall_class', 'exp_field_class']]
# columnsToHotEncode = ['country', 'industry','gender']


def prepare_data(country, industry, education, gender, age, experience_overall, experience_field):
    data = pd.DataFrame({
        "country": [country],
        "industry": [industry],
        "education_level": [education],
        "gender": [gender],
        "age": [age],
        "experience_overall": [experience_overall],
        "experience_field": [experience_field]
    })

    # Mapping
    process_education(data)
    process_age(data)
    process_experience(data)

    # Hotencoding
    process_country(data)
    process_industry(data)
    process_gender(data)

    # Fit processed data into preset dataset (that aligns with the features of the model)
    preset = preset_data.copy()
    for column in preset.columns:
        if column in data.columns:
            preset[column] = data[column]

    return preset


def process_age(data):
    # Create an age mapping to represent the order of values
    age_mapping = {
        '18-24': 1,
        '25-34': 2,
        '35-44': 3,
        '45-54': 4,
        '55-64': 5
    }

    # Apply the mapping to encode the age ranges to an additional attribute
    data['age_class'] = data['age'].map(age_mapping)

    # Drop age column
    data.drop('age', axis=1, inplace=True)


def process_experience(data):
    # Create an experience mapping to represent the order and distance of values
    # TODO: Check if float or int here is an issue for the model (e.g. 3.0 vs 3)
    replacements_exp = {
        '1': 1,
        '2-4': 3,
        '5-7': 6,
        '8-10': 9,
        '11-20': 15.5,
        '21-30': 25.5,
        '31-40': 35.5,
        '41': 41
    }

    # Apply the mappings to encode the ranges to additional attributes
    data['exp_overall_class'] = data['experience_overall'].map(
        replacements_exp)
    data['exp_field_class'] = data['experience_field'].map(replacements_exp)

    # Drop experience columns
    data.drop('experience_overall', axis=1, inplace=True)
    data.drop('experience_field', axis=1, inplace=True)


def process_education(data):
    # Replacement dictionary
    replacements_degree = {
        'High School': 1,
        'Some college': 2,
        'College degree': 3,
        "Master's degree": 4,
        'PhD': 5,
        'Professional degree (MD, JD, etc.)': 6
    }

    # Apply the mappings to encode the ranges to additional attributes
    data['education_class'] = data['education_level'].map(replacements_degree)

    # Drop education column
    data.drop('education_level', axis=1, inplace=True)


def process_gender(data):
    # Manual hotencoding, first add columns "gender_Other" and "gender_Woman" with False
    data['gender_Other'] = False
    data['gender_Woman'] = False

    gender = data.loc[0, 'gender']

    if gender == 'male':
        pass
    elif gender == 'female':
        data['gender_Woman'] = True
    else:
        data['gender_Other'] = True

    # Drop column "gender"
    data.drop('gender', axis=1, inplace=True)


def process_country(data):
    # Manual hotencoding, first add columns for each country with False
    country_columns = [
        'country_united states', 'country_united kingdom', 'country_canada', 'country_netherlands',
        'country_australia', 'country_spain', 'country_france', 'country_germany', 'country_ireland',
        'country_denmark', 'country_switzerland', 'country_bermuda', 'country_mexico', 'country_south africa',
        'country_belgium', 'country_sweden', 'country_hong kong', 'country_kuwait', 'country_sri lanka',
        'country_greece', 'country_austria', 'country_luxembourg', 'country_new zealand', 'country_latvia',
        'country_finland', 'country_puerto rico', 'country_rwanda', 'country_united arab emirates', 'country_romania',
        'country_serbia', 'country_russia', 'country_japan', 'country_china', 'country_cambodia', 'country_vietnam',
        'country_bangladesh', 'country_israel', 'country_lithuania', 'country_eritrea', 'country_italy',
        'country_slovenia', 'country_somalia', 'country_norway', 'country_malaysia', 'country_slovakia',
        'country_portugal', 'country_india', 'country_sierra leone', 'country_england', 'country_singapore',
        'country_the bahamas', 'country_costa rica', 'country_argentina', 'country_chile', 'country_qatar',
        'country_hungary', 'country_brazil', 'country_uruguay', 'country_uganda', 'country_philippines',
        'country_poland', 'country_malta', 'country_bulgaria', 'country_estonia', 'country_morocco',
        'country_ecuador', 'country_zimbabwe', 'country_ghana', 'country_croatia', 'country_south korea',
        'country_thailand', 'country_isle of man', 'country_jamaica', 'country_kenya', 'country_jordan'
    ]

    for column in country_columns:
        data[column] = [False]

    country = data.loc[0, 'country']

    # Was the first in processing (alphabetically) and is the only one that should not have a column (drop_first=True)
    if country == 'afghanistan':
        pass

    # Set the column of the country to True
    data[f"country_{country}"] = True

    # Drop column "country"
    data.drop('country', axis=1, inplace=True)


def process_industry(data):
    # Manual hotencoding, first add columns for each industry with False
    industry_columns = [
        'industry_Agriculture or Forestry', 'industry_Art & Design', 'industry_Business or Consulting',
        'industry_Computing or Tech', 'industry_Education (Higher Education)', 'industry_Education (Primary/Secondary)',
        'industry_Engineering or Manufacturing', 'industry_Entertainment', 'industry_Government and Public Administration',
        'industry_Health care', 'industry_Hospitality & Events', 'industry_Insurance', 'industry_Law',
        'industry_Law Enforcement & Security', 'industry_LeisureSport & Tourism', 'industry_MarketingAdvertising & PR',
        'industry_Media & Digital', 'industry_Nonprofits', 'industry_Other', 'industry_Property or Construction',
        'industry_Recruitment or HR', 'industry_Retail', 'industry_Sales', 'industry_Social Work',
        'industry_Transport or Logistics', 'industry_Utilities & Telecommunications'
    ]

    for column in industry_columns:
        data[column] = [False]

    industry = data.loc[0, 'industry']

    # First in processing (alphabetically) and is the only one that should not have a column (drop_first=True)
    if industry == 'Accounting, Banking & Finance':
        pass

    # Set the column of the industry to True
    data[f"industry_{industry}"] = True

    # Drop column "industry"
    data.drop('industry', axis=1, inplace=True)

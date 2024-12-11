import sys
import pandas as pd
import os

def help_message():
    return """Usage: countriespop <countries> [options]
<country> is a country to get population and other general information.

If the country you need information has two or more words, replace the spaces to _
For example: United_States
The tool is case-insensitive.

Options:
    -h, --help:     Display this help message (all other options are ignored if this is present)
    One or more of the following options can be used to get specific information about the country:
    --population (default): Get the population of the country
    --cca3:          Get the standaridzed country code (three-letter)
    --pop2050:       Get the projected population of the country in 2050
    --area:          Get the area of the country
    --rank:         Get the global population rank in the world
    --netchange:     Get the net change of the population of the country
    --growthrate:     Get the growth rate of the population of the country
    --density:       Get the population density of the country
    --world_percentage: Get the percentaje of the world that country represents
    --all:           Get all the information of the country
    
    """
def parse_args(args):
    """Analizes and parses the arguments given by the user
    The arguments must be a country and a list of data to get from the given country
    It returns  """
    if len(args) == 0 or ("-h" in args) or ("--help" in args):
        print(help_message())
        sys.exit(1)
    country=[]
    data=list()
    valid_data = ["help","cca3", "population", "pop2050", "area", "rank", "netchange", "growthrate", "density", "world_percentage", "all"]    
    
    countries = [
        "India", "Central_African_Republic", "Burkina_Faso", "Brunei", "Uganda", "Gabon", 
        "Honduras", "Dominica", "China", "Finland", "Syria", "Bahamas", "Sudan", "Lesotho", 
        "Czech_Republic", "Cayman_Islands", "United_States", "Norway", "Sri_Lanka", "Belize", 
        "Spain", "Guinea-Bissau", "Azerbaijan", "Bermuda", "Indonesia", "Liberia", "Malawi", 
        "Guadeloupe", "Argentina", "Slovenia", "Greece", "Guernsey", "Pakistan", "Palestine", 
        "Zambia", "Iceland", "Algeria", "North_Macedonia", "Papua_New_Guinea", "Greenland", 
        "Nigeria", "Lebanon", "Romania", "Martinique", "Iraq", "Latvia", "Portugal", 
        "Faroe_Islands", "Brazil", "New_Zealand", "Chile", "Mayotte", "Afghanistan", 
        "Equatorial_Guinea", "Hungary", "Northern_Mariana_Islands", "Bangladesh", "Costa_Rica", 
        "Kazakhstan", "Vanuatu", "Poland", "Trinidad_And_Tobago", "Tajikistan", 
        "Saint_Kitts_And_Nevis", "Russia", "Ireland", "Chad", "French_Guiana", "Canada", 
        "Bahrain", "United_Arab_Emirates", "Turks_And_Caicos_Islands", "Mexico", "Mauritania", 
        "Ecuador", "French_Polynesia", "Morocco", "Timor-Leste", "Belarus", "Sint_Maarten", 
        "Ethiopia", "Oman", "Somalia", "New_Caledonia", "Saudi_Arabia", "Estonia", "Israel", 
        "American_Samoa", "Japan", "Panama", "Guatemala", "Barbados", "Ukraine", "Mauritius", 
        "Togo", "Marshall_Islands", "Philippines", "Kuwait", "Senegal", "Sao_Tome_And_Principe", 
        "Angola", "Cyprus", "Austria", "Liechtenstein", "Egypt", "Croatia", "Netherlands", 
        "Samoa", "Uzbekistan", "Eswatini", "Switzerland", "Monaco", "DR_Congo", "Eritrea", 
        "Cambodia", "Curacao", "Yemen", "Djibouti", "Sierra_Leone", "San_Marino", "Vietnam", 
        "Georgia", "Zimbabwe", "Saint_Lucia", "Peru", "Reunion", "Laos", "Gibraltar", "Iran", 
        "Mongolia", "Guinea", "Guam", "Malaysia", "Fiji", "Hong_Kong", "Saint_Martin", "Turkey", 
        "Moldova", "Rwanda", "Kiribati", "Ghana", "Comoros", "Serbia", "British_Virgin_Islands", 
        "Germany", "Uruguay", "Benin", "Grenada", "Mozambique", "Guyana", "Nicaragua", "Palau", 
        "Thailand", "Puerto_Rico", "Burundi", "Micronesia", "Nepal", "Bhutan", "Libya", 
        "Cook_Islands", "United_Kingdom", "Bosnia_And_Herzegovina", "Tunisia", "Jersey", 
        "Madagascar", "Solomon_Islands", "Paraguay", "Anguilla", "Tanzania", "Albania", "Bolivia", 
        "Tonga", "Ivory_Coast", "Macau", "Kyrgyzstan", "Nauru", "France", "Jamaica", "Haiti", 
        "Seychelles", "Venezuela", "Luxembourg", "Bulgaria", "Wallis_And_Futuna", "South_Africa", 
        "Armenia", "Belgium", "Aruba", "Cameroon", "Montenegro", "Turkmenistan", "Tuvalu", 
        "Italy", "Gambia", "Jordan", "Saint_Vincent_And_the_Grenadines", "Niger", "Suriname", 
        "El_Salvador", "Saint_Barthelemy", "Kenya", "Lithuania", "Dominican_Republic", 
        "United_States_Virgin_Islands", "Australia", "Cape_Verde", "Republic_of_the_Congo", 
        "Saint_Pierre_And_Miquelon", "Myanmar", "Qatar", "Cuba", "Antigua_And_Barbuda", 
        "North_Korea", "Western_Sahara", "Singapore", "Montserrat", "Colombia", "Botswana", 
        "South_Sudan", "Isle_Of_Man", "Taiwan", "Malta", "Denmark", "Falkland_Islands", 
        "South_Korea", "Namibia", "Sweden", "Andorra", "Mali", "Maldives", "Slovakia", "Niue", 
        "Vatican_City", "Tokelau"
        ]
    for arg in args:
        if arg.startswith("--") or arg.startswith("-"):
            if arg.startswith("--"):
                data_name = arg.strip("--")
                if data_name=="help":
                    print(help_message())
                    sys.exit(1)
            else:
                data_name = arg.strip("-")
                if data_name=="h":
                    print(help_message())
                    sys.exit(1)
            if data_name not in valid_data:
                print(f"Error: Data must be one of '{valid_data}'")
                sys.exit(1)
            else:
                data.append(data_name)
        elif arg.title() in countries:
            country.append(arg)
        else:
            print(f"Error: Sorry, there's no information about '{arg}'")
            sys.exit(1)
    if len(country) >1:
        print("Error: Please, only one country is allowed\n")
        print(help_message())
        sys.exit(1)
    if len(data) == 0:
        data.append("population") # Default data if no argument is given
    return country, data #both are lists


def info(country,data):
    """Gets the information of the country given by the user
    As arguments, recieves the argumetns given by the user already parsed by the parse_args function
    So we're completely sure that the arguments are valid."""

    current_dir = os.path.dirname(__file__) # Path to the current directory
    csv_path = os.path.join(current_dir, "data", "countries_table.csv") # Path to the csv file
    df = pd.read_csv(csv_path) # Read the csv file
    df_dict=df.to_dict(orient="records")   # the "orient = "records" " argument converts the dataframe to a list of dictionaries
    for c in country:
        count=next(item for item in df_dict if item['country'].title()==c.title())
    i=0
    results=[]
    percentaje=float(count['worldPercentage'])
    for c in count:
        while i <=len(data)-1:
            if data[i]=="all":
                results.append(f"Country: {count['country']}\nPopulation: {count['pop2023']}\nProjected Population in 2050: {count['pop2050']}\nArea: {count['area']}\nGlobal Population Rank: {count['rank']}\nNet Change: {count['netChange']}\nGrowth Rate: {count['growthRate']}\nPopulation Density: {count['density']}\nWorld Percentage: {count['worldPercentage']}")
            elif data[i]=="population":
                results.append(f"The population of {count['country']} is {count['pop2023']}")
            elif data[i]=="cca3":
                results.append(f"The standardized country code of {count['country']} is {count['cca3']}")
            elif data[i]=="pop2050":
                results.append(f"The projected population of {count['country']} in 2050 is {count['pop2050']}")
            elif data[i]=="area":
                results.append(f"The area of {count['country']} is {count['area']} km2")
            elif data[i]=="rank":
                results.append(f"The global population rank of {count['country']} is {count['rank']}")
            elif data[i]=="netchange":
                results.append(f"The net change of the population of {count['country']} is {count['netChange']}")
            elif data[i]=="growthrate":
                results.append(f"The growth rate of the population of {count['country']} is {count['growthRate']}")
            elif data[i]=="density":
                results.append(f"The population density of {count['country']} is {count['density']}")
            elif data[i]=="world_percentage":
                results.append(f"The percentage of the world that {count['country']} represents is {percentaje*100}%")
            
            i+=1
    return "\n\n".join(results)
def main ():
    args=sys.argv[1:]
    (country,data)=parse_args(args)
    print(info(country, data))

if __name__ == "__main__":
    main()
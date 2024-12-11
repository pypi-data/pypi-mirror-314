from module import test

# create a dictionary
data = {'Name': ['John', 'Alice', 'Bob'],
       'Age': [25, 30, 35],
       'City': ['New York', 'London', 'Paris']}

def main():
    df = test(data)
    print(df)

if __name__ == '__main__':
    main()
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
#基本数据建立
start_date="2021-01-01"
end_date="2024-12-31"
dates=pd.date_range(start_date,end_date,freq="D")
fruits=["香蕉","苹果","葡萄","橙子","哈密瓜","芭乐","梨","桃子"]
customers=["Mike" ,"John" ,"Tom" ,"xiaoming" ,"Jimmy" ,"Lym" ,"Michk"]
random_fruits=[random.choice(fruits) for _ in range(len(dates))]
random_customers=[random.choice(customers) for _ in range(len(dates))]
random_weights=np.random.uniform(50,100,len(dates)).round(0)
order=pd.DataFrame({"date":dates,"fruit":random_fruits,"customer":random_customers,"weight(kg)":random_weights})
random_prices=np.random.uniform(1.0,20.0,len(fruits)).round(2)
region=["西北","华中","华南","华北"]
random_region=[random.choice(region) for _ in range(len(fruits))]
info=pd.DataFrame({"fruit":fruits,"price":random_prices,"region":random_region})
df=pd.merge(order,info,on="fruit")
df=df.sort_values(by="date",ascending=True).reset_index(drop=True)
df["amount"]=df["price"]*df["weight(kg)"]
df["year"]=df["date"].dt.year
df["month"]=df["date"].dt.month
df["year_month"]=df["date"].dt.year*100+df["date"].dt.month
print(df)
#销量统计
monthly_sale_weights=df.groupby("year_month")["weight(kg)"].sum().reset_index()
monthly_sale_weights.plot(kind="bar",x="year_month",y="weight(kg)",figsize=(16,9))
plt.title("月销量")
monthly_sale_amounts=df.groupby("year_month")["amount"].sum().reset_index()
monthly_sale_amounts.plot(kind="line",x="year_month",y="amount",figsize=(16,9))
plt.title("月销售额")
plt.show()
year_summary=df.groupby("year").agg({"weight(kg)":"sum","amount":"sum"}).reset_index()
year_summary["average_amount"]=(year_summary["amount"]/year_summary["weight(kg)"]).round(2)
print(year_summary)
fruit_year_sales=df.groupby(["fruit","year"])["weight(kg)"].sum().reset_index()
for year in range(2021,2025):
    year_data = fruit_year_sales[fruit_year_sales["year"] == year]

    plt.figure(figsize=(8, 8))
    plt.pie(
        year_data["weight(kg)"],
        labels=year_data["fruit"],
        autopct="%1.1f%%"
    )
    plt.title(f"{year}年度销售金额占比")
plt.show()
for fruit in fruits:
    fruit_data = fruit_year_sales[fruit_year_sales["fruit"] == fruit]

    plt.figure(figsize=(8, 8))
    plt.pie(
        fruit_data["weight(kg)"],
        labels=fruit_data["year"],
        autopct="%1.1f%%",
    )

    plt.title(f"{fruit}各年度销售金额占比")
plt.show()
stack_df = df.groupby(["year_month","fruit"])["weight(kg)"].sum().reset_index()
pivot_data = stack_df.pivot(index="year_month",columns="fruit",values="weight(kg)").fillna(0)
pivot_data.plot(kind="bar",stacked=True,figsize=(16,9))
plt.title("各水果月度累积销量堆叠柱状图")
plt.xlabel("year_month")
plt.ylabel("weight(kg)")
plt.show()
#用户复购周期分析
user_df = df.sort_values(by=["customer", "date"]).reset_index(drop=True)
user_df['pre_date'] = user_df.groupby('customer')['date'].shift(1)
user_df['gap_day'] = (user_df['date'] - user_df['pre_date']).dt.days
repurchase = user_df.dropna(subset=['gap_day']).copy()
customer_repurchase = repurchase.groupby('customer').agg(
    count=('gap_day', 'count'),
    mean=('gap_day', 'mean')
).reset_index()
print(customer_repurchase)
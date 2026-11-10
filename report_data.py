import pandas as pd
import numpy as np
import matplotlib as plt


class file:
    def __init__(self, data):
        self.f_path = data.copy()

        self.f_path["Production_Date"] = pd.to_datetime(
            self.f_path["Production_Date"],
            errors="coerce"
        )
    def format_date(self):
        self.f_path["Production_Date"] = self.f_path["Production_Date"].dt.strftime("%#d-%#m-%y")
        return self.f_path

    def head(self):
        return self.f_path.head()
 
    def tail(self):
        return self.f_path.tail()

    def column_names(self):
        columns =  self.f_path.columns
        
        for column in columns:
            print(column)

    def data_types(self):
        return self.f_path.dtypes

    def columns_strip(self):
        self.f_path.columns = self.f_path.columns.str.strip()
        return self.f_path.head()

    def line(self):
        print("----"*50, "\n")
    
    def describe(self):
        return self.f_path.describe()
        # values = self.f_path.describe()
        # for column in values.columns:
        #     print(f"Column: {column}")
        #     print(values[column])
        #     print("\n")
        
    def total_null_values(self):
        return f" Total number of null values: {self.f_path.isnull().sum().sum()}"

    def duplicate_values(self):
        return f" Total number of duplicate rows: {self.f_path.duplicated().sum()}"

    def duplicate_values_rows(self):
        return self.f_path[self.f_path.duplicated(keep=False)]

    def drop_duplicate_values(self):
        self.f_path.drop_duplicates(inplace=True)
        return f" Total no of duplicate rows after removing: {self.f_path.duplicated().sum()})"

    def customers_name(self):
        customers = self.f_path['Customer_Name'].unique()
        print("Customer Names:")
        for customer in customers:
            print(customer)

    def shift_value_change(self):
        self.f_path["Shift"] = self.f_path["Shift"].replace({
            "A":"Morning",
            "B":"Afternoon",
            "C":"Evening"
        })
        return self.f_path.head()

    def department_groupby(self):
        department = self.f_path.groupby("Department").agg(
            Planned_production = ("Planned_Production_Units","sum"),
            Total_production = ("Actual_Production_Units","sum"),
            Total_sales = ("Sales_Revenue","sum")
        ).reset_index()
        pd.set_option("display.float_format", '{:.2f}'.format) 

        return department

    def department_defects(self):
        department = self.f_path.groupby("Department").agg(
            defects = ("Defect_Units","sum")
        ).reset_index()

        department = department.sort_values(
            by="defects",
            ascending=False
        ).reset_index(drop=True)

        return department

    def plant_groupby(self):
        plant = self.f_path.groupby("Plant").agg(
            Planned_production = ("Planned_Production_Units","sum"),
            Manufacturing_cost = ("Total_Manufacturing_Cost","sum"),
            Total_production = ("Actual_Production_Units","sum"),
            Total_sales = ("Sales_Revenue","sum")
        ).reset_index()
        pd.set_option("display.float_format", "{:.2f}".format)

        return plant

    def plant_dept_groupby(self):
        pld = self.f_path.groupby(["Plant","Department"])["Actual_Production_Units"].sum().unstack()
        pd.set_option("display.float_format","{:.2f}".format)

        return pld

    def shift_groupby(self):
        shift = self.f_path.groupby("Shift").agg(
            Planned_production = ("Planned_Production_Units","sum"),
            Manufacturing_cost = ("Total_Manufacturing_Cost","sum"),
            Total_Production = ("Actual_Production_Units","sum"),
            Total_sales = ("Sales_Revenue","sum")
        ).reset_index()
        pd.set_option("display.float_format","{:.2f}".format)

        return shift

    def customer_groupby(self):
        customers = self.f_path.groupby("Customer_ID").agg(
            Customer_Name = ("Customer_Name", "first"),
            Total_sales = ("Sales_Revenue", "sum")
        ).reset_index()
        pd.set_option("display.float_format","{:.2f}".format)

        return customers

    def material_groupby(self):
        materials = self.f_path.groupby("Raw_Material").agg(
            total_production = ("Actual_Production_Units","sum"),
            total_defects = ("Defect_Units","sum"),
            total_manufacturing_cost = ("Total_Manufacturing_Cost","sum")
        ).reset_index()

        return materials

    def ProductCategory_groupby(self):
        product = self.f_path.groupby("Product_Category").agg(
            planned_production = ("Planned_Production_Units","sum"),
            total_production = ("Actual_Production_Units","sum"),
            manufacturing_cost = ("Total_Manufacturing_Cost","sum"),
            defective_units = ("Defect_Units","sum"),
            total_sales = ("Sales_Revenue","sum")
        ).reset_index()

        pd.set_option("display.float_format","{:.2f}".format)
        
        return product

    def date_groupby(self):
        date = self.f_path.groupby("Production_Date").agg(
            planned_production = ("Planned_Production_Units","sum"),
            total_production = ("Actual_Production_Units","sum"),
            total_sales = ("Sales_Revenue","sum")
        ).reset_index()


        date["Production_Date"] = pd.to_datetime(date["Production_Date"],format="%#d-%#m-%y",errors="coerce")
        date["Month"] = (date["Production_Date"].dt.to_period("M"))
        date["Production_Date"] = date["Production_Date"].dt.strftime("%#d-%#m-%y")
        date["Month"]= (date["Month"].dt.strftime("%#m-%y"))

        pd.set_option("display.float_format"," {:.2f}".format)

        return date

    def sales_channel_groupby(self):
        region = self.f_path.groupby("Sales_Channel").agg(
            total_sales = ("Sales_Revenue","sum"),
            total_production = ("Actual_Production_Units","sum")
        ).reset_index()

        pd.set_option("display.float_format","{:.2f}".format)

        return region

    def machine_downtime(self):
        machines = self.f_path.groupby("Machine_ID").agg(
            downtime_mins = ("Downtime_Minutes","sum")
        ).reset_index()

        machines = machines.sort_values(
            by="downtime_mins",
            ascending=False
        ).reset_index(drop = True)

        return machines

    def sales_region_groupby(self):
        region = self.f_path.groupby("Sales_Region").agg(
            total_sales = ("Sales_Revenue","sum")
        ).reset_index()

        pd.set_option("display.float_format","{:.2f}".format)

        return region

    # def to_excel(self,path):
    #     self.f_path.to_excel(path, index=False)
    #     print(f"File saved to {path}")

class excel_file(file):
    def to_excel(self):
        try:
            f_path = input("Enter the folder path to save:").strip('"')
            with pd.ExcelWriter(f_path, engine='openpyxl') as writer:
                self.f_path.to_excel(writer, sheet_name='Cleaned Data', index=False)
                self.department_groupby().to_excel(writer, sheet_name='Department', index=False)
                self.plant_groupby().to_excel(writer, sheet_name='Plant', index=False)
                self.shift_groupby().to_excel(writer, sheet_name='Shift', index=False)
                self.customer_groupby().to_excel(writer, sheet_name='Customer', index=False)
                self.material_groupby().to_excel(writer, sheet_name='Material', index=False)
                self.ProductCategory_groupby().to_excel(writer, sheet_name='ProductCategory', index=False)
                self.date_groupby().to_excel(writer,sheet_name='Date',index=False)
                self.sales_region_groupby().to_excel(writer, sheet_name='Region', index=False)
                self.sales_channel_groupby().to_excel(writer, sheet_name='Sales Channel', index=False)
                print("File saved to your path successfully")
        except Exception as e:
            print(f"An error occurred while saving the Excel file: {e}")

class chart(excel_file):
    def revenue_by_department(self):
        department = self.department_groupby()

        bars = plt.bar(
            department["Department"],
            department["Total_sales"]
        )
        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                bar.get_height(),
                ha="center",
                va="bottom"
            )

        plt.title("Revenue By Department")
        plt.xlabel("Department")
        plt.ylabel("Sales")
        plt.grid(axis="y"),
        plt.ticklabel_format(style="plain",axis="y")
        
        return plt.show()

    def revenue_by_product(self):
        product = self.ProductCategory_groupby()

        bars = plt.bar(
            product["Product"],
            product["Total_sales"]
        )

    def department_spider_chart(self):

        department = self.department_groupby()

        categories = department["Department"].tolist()
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"polar": True})

        for column, label, offset in [
            ("Planned_production", "Planned Production", -10),
            ("Total_production", "Actual Production", 10)
        ]:

            values = department[column].tolist()
            values += values[:1]

            ax.plot(angles, values, linewidth=2, label=label)
            ax.fill(angles, values, alpha=0.1)

            for angle, value in zip(angles[:-1], values[:-1]):
                ax.annotate(
                    f"{value:,.0f}",
                    (angle, value),
                    xytext=(offset, offset),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8
                )


        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.tick_params(axis="x", pad=20)

        ax.set_title("Planned vs Actual Production by Department", pad=30)
        ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1))

        plt.tight_layout()
        return plt.show()

    def plant_radar_chart(self):
        plant = self.plant_groupby()

        plant["Target_Sales"] = 149000000

        categories = plant["Plant"].tolist()

        angles = np.linspace(
            0,2*np.pi,
            len(categories),
            endpoint=False
        ).tolist()

        angles += angles[:1]
        actual = plant["Total_sales"].tolist()
        target = plant["Target_Sales"].tolist()

        actual += actual[:1]
        target += target[:1]

        fig, ax = plt.subplots(
            figsize = (9,9),
            subplot_kw= {"polar" : True}
        )

        for values , label in [
            (actual,"Total_sales"),
            (target,"Target_sales")
        ]:
            ax.plot(angles,values,linewidth = 2,label=label)
            ax.fill(angles,values,alpha = 0.1)

            for angle , value in zip(angles[:-1],values[:-1]):
                ax.annotate(
                    f"{value:.0f}",
                    (angle,value),
                    xytext = (5,8),
                    textcoords = "offset points",
                    ha="center",
                    fontsize=8
                )

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        ax.set_title("Actual Sales vs Target Sales",pad=25)
        ax.legend(loc="upper right",bbox_to_anchor = (1.3,1.1))
        plt.tight_layout()

        return plt.show()

    def product_radar_chart(self):
        product = self.ProductCategory_groupby()

        product["Target_sales"] = 113400000

        categories = product["Product_Category"].tolist()

        angles = np.linspace(
            0,2*np.pi,
            len(categories),
            endpoint=False
        ).tolist()

        angles += angles[:1]
        # actual = product["total_sales"].tolist()
        # target = product["Target_Sales"].tolist()


        # actual += actual[:1]
        # target += target[:1]
        archievement = (product["total_sales"]/product["Target_sales"])*100
        archievement = archievement.tolist()
        archievement += archievement[:1]

        target_percentage = [100] * len(archievement)

        fig, ax = plt.subplots(
            figsize = (9,9),
            subplot_kw= {"polar" : True}
        )

        # for values , label in [
        #     (actual,"total_sales"),
        #     (target,"Target_sales")
        # ]:
        ax.plot(
            angles, archievement,
            linewidth=2,
            label="Actual Sales Achievement"
        )
        ax.fill(angles, archievement, alpha=0.1)


        ax.plot(angles,target_percentage,linewidth = 2,label="Target Sales (100%)")
        ax.fill(angles,target_percentage,alpha = 0.05)

        for angle , value in zip(angles[:-1],archievement[:-1]):
            ax.annotate(
                f"{value:.0f}%",
                (angle,value),
                xytext = (5,8),
                textcoords = "offset points",
                ha="center",
                fontsize=8
            )

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)


        # ax.set_ylim(0, 120)
        # ax.set_ylabel("Sales Achievement (%)")

        ax.set_title("Actual Sales vs Target",pad=25)
        ax.legend(loc="upper right",bbox_to_anchor = (1.3,1.1))
        # ax.legend(product["total_sales"],loc="upper right",bbox_to_anchor = (1.3,1.1))
        plt.tight_layout()

        return plt.show()

    def date_chart(self):
        date = self.date_groupby()

        plt.figsize = (8,8)

        plt.plot(
            date["Production_Date"],
            date["planned_production"],
            marker="o",
            linewidth = 2,
            label = "Target Production"
        )

        plt.plot(
            date["Production_Date"],
            date["total_production"],
            marker = "o",
            linewidth = 2,
            label = "Actual Production"
        )


        plt.title("Planned production vs Actual Production")
        plt.xlabel("Production Month")
        plt.ylabel("Production Units")
        plt.xticks(rotation=90)
        plt.grid(axis="y")
        plt.legend()

        plt.tight_layout()
        return plt.show()

    def material_defect_chart(self):
        materials = self.material_groupby()

        bars = plt.bar(
            materials["Raw_Material"],
            materials["total_defects"],
            color="#DC5656"
        )
        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                f"{bar.get_height():.0f}",
                ha="center",
                va="bottom"
            )

        plt.title("Defects By Materials")
        plt.xlabel("Materials")
        plt.ylabel("Defects")
        plt.grid(axis="y"),
        plt.ticklabel_format(style="plain",axis="y")

        return plt.show()

    def production_achievement_chart(self):
        production = self.date_groupby()

        target = production["planned_production"].sum()
        actual = production["total_production"].sum()

        achievement = (actual/target)*100 if target != 0 else 0

        fig, ax = plt.subplots(figsize = (6,3))

        ax.pie(
            [min(achievement,100),max(100-achievement,0)],
            startangle=180,
            counterclock=False,
            colors=["grey","lightgrey"],
            wedgeprops={"width":0.3}
        )

        ax.text(
            0,0,
            f"{achievement:.1f}%",
            ha="center",
            va="center",
            fontsize=25,
            fontweight="bold"
        )

        ax.set_title("Overall Production Achievement")

        return plt.show()

    def plant_dept_chart(self):
        pltd = self.plant_dept_groupby()
        colors = ["#DB4444","#65A1E7","#E76AB9","#61DB77"]

        ax = pltd.plot(
            kind="bar",
            stacked=True,
            figsize=(8,6),
            color = colors
        )
        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.0f",
                label_type="center",
                fontsize = 9
            )
            
        plt.title("Plant-wise Department Production")
        plt.xlabel("Plant")
        plt.ylabel("Total Production")
        plt.legend(title="Department")
        plt.xticks(rotation = 0)
        plt.tight_layout()

        return plt.show()

    def department_defect_chart(self):
        department = self.department_defects()

        department["Total_defects"] = department["defects"].cumsum()

        department["Cumulative_percentage"] = (department["Total_defects"]/department["defects"].sum())*100

        fig, ax1 = plt.subplots(figsize = (10,6))
        ax1.bar(
            department["Department"],
            department["defects"],
            color = "#DC5656",
            label = "Defects"
        )

        ax1.set_xlabel("Department")
        ax1.set_ylabel("Number of Defects")
        ax1.set_title("Department-wise Defects Chart")

        ax2 = ax1.twinx()

        ax2.plot(
            department["Department"],
            department["Cumulative_percentage"],
            color = "red",
            marker = "o",
            label = "Cumulative Percentage"
        )
        ax2.axhline(
            y=95,
            color="lightblue",
            linestyle ="--",
            label="80% Reference"
        )
        ax2.set_ylabel("Cumulatvie Percentage")
        ax2.set_ylim(0, 110)

        return plt.show()

    def machine_downtime_chart(self):
        machine = self.machine_downtime()

        plt.figure(figsize=(10,6))

        bars = plt.barh(
            machine["Machine_ID"],
            machine["downtime_mins"],
            color = "#CA4B4B"
        )
        plt.bar_label(bars, padding=5, fmt="%.0f")

        plt.title("Machine wise Downtime Minutes")

        return plt.show()
        
    def sales_channel_distribution(self):
        sales_channel = self.f_path.groupby("Sales_Channel")["Sales_Revenue"].sum().reset_index()

        pd.set_option("display.float_format","{:.0f}".format)

        sales_channel = sales_channel.sort_values(
            by="Sales_Revenue",
            ascending=False
        ).reset_index(drop=True)

        plt.figure(figsize=(10,6))

        plt.pie(
            sales_channel["Sales_Revenue"],
            labels=sales_channel["Sales_Channel"],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"width": 0.6}
        )

        plt.legend(loc="upper right",bbox_to_anchor = (1.3,1.1))

        plt.title("Sales Channel Revenue Distribution")
        return plt.show()

    def daily_sales(self):
        sales = self.date_groupby().groupby("Month")["total_sales"].sum().reset_index()

        plt.plot(
            sales["Month"].astype(str),
            sales["total_sales"],
            marker="o",
            linewidth = 2,
            linestyle = "-"   
        )

        for x, y in zip(sales["Month"].astype(str), sales["total_sales"]):
            plt.annotate(
                f"₹{y:,.0f}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center"
            )

        plt.title("Monthly Sales Revenue")
        plt.xlabel("Month")
        plt.ylabel("total_sales")
        plt.xticks(rotation = 25)
        plt.grid(axis="both")

        return plt.show()

    def region_wise_sale(self):
        sales = self.sales_region_groupby()

        bars = plt.bar(
            sales["Sales_Region"],
            sales["total_sales"],
            color = "#8BD367"
        )

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                f"{bar.get_height():.2f}",
                ha="center",
                va="bottom"
            )
        plt.title("Region wise Sales")
        plt.xlabel("Region")
        plt.ylabel("Sales")
        plt.xticks(rotation = 25)
        plt.grid(axis="y")

        return plt.show()

    def revenue_and_manufacturing(self):
        df = self.ProductCategory_groupby()

        product = df["Product_Category"]
        sales = df["total_sales"]
        cost = df["manufacturing_cost"]

        x = range(len(product))
        width = 0.35

        plt.figure(figsize=(12,6))

        bar1 = plt.bar(
            [i - width/2 for i in x],
            sales,
            width,
            label= "Sales Revenue",
            color = "#3965BD"
        )
        bar2 = plt.bar(
            [i + width/2 for i in x],
            cost,
            width,
            label = "Manufacturing Cost",
            color = "#7DE8E6" 
        )

        plt.bar_label(bar1, labels=[f'{v/100000:.2f}L' for v in sales], padding=3, fontsize=8)
        plt.bar_label(bar2, labels=[f'{v/100000:.2f}L' for v in cost], padding=3, fontsize=8)

        plt.xticks(list(x), product, rotation=30, ha="right")

        plt.title("Sales Revenue vs Manufacturing Cost by Product")
        plt.xlabel("Product Category")
        plt.ylabel("Amount")
        plt.legend()
        plt.grid(axis="y",alpha = 0.3)
        plt.tight_layout()
        return plt.show()


# file1 = chart()

# file1.format_date()

# file1.line()
# print('Head---------------')
# print(file1.head())


# file1.line()

# print('Tail---------------------')
# print(file1.tail())

# file1.line()
# file1.column_names()

# file1.line()
# print(file1.data_types())

# # file1.line()
# # print(file1.columns_strip())

# file1.line()
# print(file1.describe())

# file1.line()
# print(file1.shift_value_change())

# file1.line()
# print(file1.total_null_values())

# file1.line()
# print(file1.duplicate_values())

# file1.line()
# print(file1.duplicate_values_rows())

# file1.line()
# print(file1.drop_duplicate_values())

# file1.line()
# print(file1.duplicate_values())

# file1.line()
# print(file1.customers_name())

# file1.line()
# print(file1.department_groupby())

# file1.line()
# print(file1.department_defects())

# file1.line()
# print(file1.plant_groupby())

# file1.line()
# print(file1.plant_dept_groupby())

# file1.line()
# print(file1.shift_groupby())

# file1.line()
# print(file1.customer_groupby())

# file1.line()
# print(file1.material_groupby())

# file1.line()
# print(file1.ProductCategory_groupby())

# file1.line()
# print(file1.date_groupby())

# file1.line()
# print(file1.sales_channel_groupby())

# file1.line()
# print(file1.machine_downtime())

# file1.line()
# file1.revenue_by_department()

# # file1.department_spider_chart()

# # file1.plant_radar_chart()

# # file1.product_radar_chart()

# # # file1.date_chart()

# # file1.material_defect_chart()

# # file1.production_achievement_chart()

# # file1.department_defect_chart()

# # file1.plant_dept_chart()

# # file1.machine_downtime_chart()

# # file1.sales_channel_distribution()

# # file1.daily_sales()

# # file1.region_wise_sale()

# # file1.revenue_and_manufacturing()

# file1.to_excel()

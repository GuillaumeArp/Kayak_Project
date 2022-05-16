Project main deliverable can be consulted [on this page](https://share.streamlit.io/guillaumearp/kayak_project/main/app.py).


Project description:

[Kayak](https://seekvectorlogo.com/wp-content/uploads/2018/01/kayak-vector-logo.png)

# Plan your trip with Kayak 

## Company's description 📇

<a href="https://www.kayak.com" target="_blank">Kayak</a> is a travel search engine that helps user plan their next trip at the best price.

The company was founded in 2004 by Steve Hafner & Paul M. English. After a few rounds of fundraising, Kayak was acquired by <a href="https://www.bookingholdings.com/" target="_blank">Booking Holdings</a> which now holds: 

* <a href="https://booking.com/" target="_blank">Booking.com</a>
* <a href="https://kayak.com/" target="_blank">Kayak</a>
* <a href="https://www.priceline.com/" target="_blank">Priceline</a>
* <a href="https://www.agoda.com/" target="_blank">Agoda</a>
* <a href="https://Rentalcars.com/" target="_blank">RentalCars</a>
* <a href="https://www.opentable.com/" target="_blank">OpenTable</a>

With over \$300 million revenue a year, Kayak operates in almost all countries and all languages to help their users book travels accros the globe. 

## Project 🚧

The marketing team needs help on a new project. After doing some user research, the team discovered that **70% of their users who are planning a trip would like to have more information about the destination they are going to**. 

In addition, user research shows that **people tend to be defiant about the information they are reading if they don't know the brand** which produced the content. 

Therefore, Kayak Marketing Team would like to create an application that will recommend where people should plan their next holidays. The application should be based on real data about:

* Weather 
* Hotels in the area 

The application should then be able to recommend the best destinations and hotels based on the above variables at any given time. 

## Goals 🎯

As the project has just started, your team doesn't have any data that can be used to create this application. Therefore, your job will be to: 

* Scrape data from destinations 
* Get weather data from each destination 
* Get hotels' info about each destination
* Store all the information above in a data lake
* Extract, transform and load cleaned data from your datalake to a data warehouse

## Scope of this project 🖼️

Marketing team wants to focus first on the best cities to travel to in France. According <a href="https://one-week-in.com/35-cities-to-visit-in-france/" target="_blank">One Week In.com</a> here are the top-35 cities to visit in France: 

```python 
["Mont Saint Michel",
"St Malo",
"Bayeux",
"Le Havre",
"Rouen",
"Paris",
"Amiens",
"Lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"Lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]
```

Your team should focus **only on the above cities for your project**. 

## Deliverable 📬

To complete this project, your team should deliver:

* A `.csv` file in an S3 bucket containing enriched information about weather and hotels for each french city

* A SQL Database where we should be able to get the same cleaned data from S3 

* Two maps where you should have a Top-5 destinations and a Top-20 hotels in the area. You can use plotly or any other library to do so. It should look something like this: 

![Map](https://full-stack-assets.s3.eu-west-3.amazonaws.com/images/Kayak_best_destination_project.png)

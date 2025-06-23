import folium
from folium.plugins import HeatMap
from preprocess import load_clean_data

def create_heatmap(property_cost1, neighborhood_group="All"):
    df = load_clean_data("data/listings.csv", neighborhood_group)
    if neighborhood_group != "All":
        df = df[df['neighbourhood_group'] == neighborhood_group]
    df['monthlyincome'] = df['price'] * (df['occupancy_rate'] / 100) * 30
    property_cost = property_cost1
    df['estimated_roi'] = (df['monthlyincome'] * 12) / property_cost * 100

    base_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    heat_data = df[['latitude', 'longitude' , "occupancy_rate"]].values.tolist()
    HeatMap(heat_data, radius=10, max_zoom=13, name="Occupancy Heatmap").add_to(base_map)
    top_df = df.sort_values(by=['estimated_roi'], ascending=False).head(200)
    top5 = df.sort_values(by='estimated_roi', ascending=False).head(5)
    for _, row in top_df.iterrows():
        popup_text = (
            f"<b>Price:</b> ${row['price']:.2f}<br>"
            f"<b>Occupancy Rate:</b> {row['occupancy_rate']:.1f}%<br>"
            f"<b>Estimated ROI:</b> {row['estimated_roi']:.2f}%"
        )
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=4,
            color='blue',
            fill=True,
            fill_opacity=0.6,
            popup=folium.Popup(popup_text, max_width=250)
        ).add_to(base_map)


    base_map.save("data/map.html")
    print("Map with 200 ROI listing created")
    return top5[['neighbourhood', 'price', 'occupancy_rate', 'estimated_roi']].to_dict(orient="records")

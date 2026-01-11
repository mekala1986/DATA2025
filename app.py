st.subheader("Movie Dataset Preview")

# 🔹 Sort option
sort_order = st.selectbox(
    "Order by Rating",
    ["Highest to Lowest", "Lowest to Highest"]
)

# 🔹 Apply sorting AFTER filtering
if sort_order == "Highest to Lowest":
    filtered_df = filtered_df.sort_values(by="rating", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="rating", ascending=True)

# 🔹 Reset index (THIS IS VERY IMPORTANT)
filtered_df = filtered_df.reset_index(drop=True)

# 🔹 Display
st.dataframe(filtered_df)

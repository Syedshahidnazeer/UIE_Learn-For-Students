import streamlit as st
from utils.virtual_economy import VirtualEconomy
from utils.auth import Auth

def format_item_card(item_id, item_data, user_coins):
    can_afford = user_coins >= item_data['price']
    color = "green" if can_afford else "red"
    
    return f"""
    <div style="border: 1px solid #ddd; padding: 10px; margin: 5px; border-radius: 5px;">
        <h3>{item_data['name']}</h3>
        <p style="color: {color};">{item_data['price']} coins</p>
        <p><small>{item_data['type'].capitalize()}</small></p>
    </div>
    """

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first")
        st.stop()

    st.title("Virtual Shop")
    
    economy = VirtualEconomy()
    auth = Auth()
    
    # Get user data
    user_data = auth.get_user_data(st.session_state.username)
    if not user_data:
        st.error("Could not load user data")
        st.stop()
    
    # Show user's coins
    st.sidebar.title("Your Wallet")
    st.sidebar.metric("Coins", user_data['coins'])
    
    # Check daily streak
    streak = economy.check_daily_streak(st.session_state.username)
    if streak > 0:
        st.sidebar.success(f"🔥 {streak} Day Streak!")
    
    # Show inventory
    st.sidebar.title("Your Inventory")
    inventory = economy.get_user_inventory(st.session_state.username)
    if inventory:
        for item in inventory:
            st.sidebar.markdown(f"- {item['item_id']} ({item['type']})")
    else:
        st.sidebar.info("Your inventory is empty")
    
    # Shop items
    st.header("Available Items")
    shop_items = economy.get_shop_items()
    
    tabs = st.tabs(list(shop_items.keys()))
    
    for tab, (category, items) in zip(tabs, shop_items.items()):
        with tab:
            cols = st.columns(2)
            for idx, (item_id, item_data) in enumerate(items.items()):
                with cols[idx % 2]:
                    st.markdown(format_item_card(item_id, item_data, user_data['coins']), unsafe_allow_html=True)
                    if st.button(f"Purchase {item_data['name']}", key=item_id):
                        success, message = economy.purchase_item(st.session_state.username, item_id)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

if __name__ == "__main__":
    main()

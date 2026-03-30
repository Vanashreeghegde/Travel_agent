# front end - capability

import streamlit as st
from agent import TravelAgent
import config

def main():
    st.set_page_config(page_title="AI Travel Planner", page_icon='✈️')
    st.title("✈️ AI Travel Planner Agent")

    @st.cache_resource
    def get_agent():
        return TravelAgent()
    agent = get_agent()

    # initialize session state
    if 'answers' not in st.session_state:
        st.session_state.answers = []
        st.session_state.current_q = 0
        st.session_state.planning_done = False

    # show questions
    if not st.session_state.planning_done:
        current_q = st.session_state.current_q

        # ── Progress Bar ──
        progress = current_q / len(config.QUESTIONS)
        st.progress(progress)
        st.caption(f"Step {current_q + 1} of {len(config.QUESTIONS)}")

        if current_q < len(config.QUESTIONS):
            st.subheader(f"Question {current_q + 1} of {len(config.QUESTIONS)}")
            st.write(config.QUESTIONS[current_q])

            answer = ""

            # different inputs for different questions
            if current_q == 0:
                col1, col2 = st.columns(2)
                with col1:
                    dest = st.text_input("Destination")
                with col2:
                    dates = st.text_input("Dates : e.g. March 15-20, 2025")
                answer = f"{dest} in {dates}" if dest and dates else ""

            elif current_q == 1:
                answer = str(st.number_input("Days", min_value=1, max_value=30, value=5))

            elif current_q == 2:
                budget = st.number_input("Budget in Euro", min_value=100, value=1000)
                answer = str(budget)

            elif current_q == 3:
                answer = st.text_input("Nationality")

            elif current_q == 4:
                st.write("Select your interests (choose multiple):")
                col1, col2, col3 = st.columns(3)
                with col1:
                    culture = st.checkbox("🏛️ Culture")
                    food = st.checkbox("🍽️ Food")
                    local_market = st.checkbox("🛍️ Local Markets")
                with col2:
                    nature = st.checkbox("🌿 Nature")
                    nightlife = st.checkbox("🌙 Nightlife")
                    adventure = st.checkbox("🧗 Adventure")
                with col3:
                    shopping = st.checkbox("🛒 Shopping")
                    history = st.checkbox("🏰 History")
                    wellness = st.checkbox("🧘 Wellness")

                custom_interest = st.text_input("Or type your own interests:")

                # combine all in one place
                selected = []
                if culture: selected.append("culture")
                if food: selected.append("food")
                if local_market: selected.append("local markets")
                if nature: selected.append("nature")
                if nightlife: selected.append("nightlife")
                if adventure: selected.append("adventure")
                if shopping: selected.append("shopping")
                if history: selected.append("history")
                if wellness: selected.append("wellness")
                if custom_interest: selected.append(custom_interest)

                answer = ", ".join(selected) if selected else ""

            # ── Travel Style ──
            elif current_q == 5:
                answer = st.selectbox(
                    "Your travel style:",
                    ["🎒 Backpacker", "👨‍👩‍👧 Family", "💎 Luxury", "🧍 Solo", "💑 Couple"]
                )

            # ── Pace of Travel ──
            elif current_q == 6:
                answer = st.radio(
                    "Preferred pace of travel:",
                    ["😌 Relaxed", "🚶 Moderate", "🏃 Packed"]
                )

            # ── Single Next Button with unique key ──
            if st.button("Next", key=f"next_btn_{current_q}"):
                if answer:
                    st.session_state.answers.append(answer)
                    st.session_state.current_q += 1
                    st.rerun()  # always do this else it wont work
                else:
                    st.warning("⚠️ Please answer the question before continuing!")

        else:
            with st.spinner("Planning your trip..."):
                itinerary = agent.plan_trip(st.session_state.answers)
            st.session_state.itinerary = itinerary
            st.session_state.planning_done = True
            st.rerun()

    # ── Itinerary Ready ──
    else:
        st.success("Your itinerary is ready!")
        st.markdown(st.session_state.itinerary)

        st.download_button(
            "Download Itinerary",
            st.session_state.itinerary,
            file_name="travel_itinerary.md",
            mime="text/markdown"
        )

        st.divider()

        # ── Extra Info Sections in 2 columns ──
        col1, col2 = st.columns(2)

        with col1:

            # ── Restaurant Recommendations within Budget ──
            with st.expander("🍽️ Restaurant Recommendations (Within Your Budget)"):
                try:
                    budget = float(st.session_state.answers[2])
                except:
                    budget = 1000

                if budget < 500:
                    st.markdown("#### 💰 Budget-Friendly Options")
                    st.write("🍜 **Street Food Stalls** — Authentic & cheapest option")
                    st.write("🥘 **Local Canteens / Dhabas** — Meals under €5")
                    st.write("🧆 **Food Markets** — Variety at low cost")
                    st.write("🥪 **Bakeries & Cafes** — Quick bites under €3")
                    st.info("💡 Eat where locals eat — cheaper and more authentic!")

                elif budget < 1500:
                    st.markdown("#### 🍽️ Mid-Range Options")
                    st.write("🍝 **Casual Dining** — €10–20 per meal")
                    st.write("🍣 **Local Cuisine Restaurants** — Best authentic experience")
                    st.write("🥗 **Bistros & Cafes** — Great for lunch, €8–15")
                    st.write("🍕 **Popular Chain Restaurants** — Consistent quality")
                    st.info("💡 Try lunch menus — same quality as dinner but cheaper!")

                else:
                    st.markdown("#### 💎 Fine Dining Options")
                    st.write("🥩 **Fine Dining** — €40–80 per person")
                    st.write("🍾 **Rooftop Restaurants** — Premium experience")
                    st.write("🦞 **Seafood & Specialty Cuisine** — Top rated spots")
                    st.write("🍱 **Michelin Star Restaurants** — If available")
                    st.info("💡 Book fine dining in advance — fills up fast!")

                st.divider()
                st.markdown("**🔍 How to Find Best Restaurants:**")
                st.write("• **Google Maps** → filter by rating 4.0+")
                st.write("• **TripAdvisor** → traveller reviews")
                st.write("• Ask **hotel staff** for local recommendations")

            # ── General Travel Tips ──
            with st.expander("💡 General Travel Tips"):
                st.write("✅ Always carry a photocopy of your passport")
                st.write("✅ Keep emergency cash separate from wallet")
                st.write("✅ Download offline maps before travelling")
                st.write("✅ Carry a universal travel adapter")
                st.write("✅ Keep hotel address written in local language")
                st.write("✅ Try local street food — but safely!")

            # ── What to Explore ──
            with st.expander("🗺️ What to Explore While Travelling"):
                st.write("🏛️ Local landmarks & museums")
                st.write("🍽️ Street food & local restaurants")
                st.write("🛍️ Local markets & souvenirs")
                st.write("🌿 Parks, nature & scenic spots")
                st.write("🚌 Local transport experience")
                st.write("🎭 Cultural shows & festivals")
                st.write("📸 Hidden gems & photo spots")

        with col2:

            # ── Nearby Hospitals & Medical Help ──
            with st.expander("🏥 Nearby Hospitals & Medical Help"):
                st.warning("⚠️ Always carry your travel insurance documents!")

                st.markdown("#### 🚑 How to Find Nearest Hospital")
                st.write("1. **Google Maps** → Search 'hospital near me'")
                st.write("2. **Ask hotel staff** — they always know")
                st.write("3. **Call emergency number** for ambulance")

                st.divider()
                st.markdown("#### 📞 Emergency Numbers by Region")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**🇮🇳 India**")
                    st.write("🚑 Ambulance: 108")
                    st.write("🚔 Police: 100")
                    st.markdown("**🇺🇸 USA**")
                    st.write("🚑 Emergency: 911")
                    st.markdown("**🇬🇧 UK**")
                    st.write("🚑 Emergency: 999")
                    st.write("🏥 NHS: 111")
                with col_b:
                    st.markdown("**🇪🇺 Europe**")
                    st.write("🚑 Emergency: 112")
                    st.markdown("**🇦🇺 Australia**")
                    st.write("🚑 Emergency: 000")
                    st.markdown("**🌐 International**")
                    st.write("SOS: +65 6338 7800")

                st.divider()
                st.markdown("#### 💊 Basic Medical Kit to Carry")
                st.write("☐ Paracetamol / Pain relievers")
                st.write("☐ Antidiarrheal medicine")
                st.write("☐ Antihistamine tablets")
                st.write("☐ Band-aids & antiseptic cream")
                st.write("☐ Rehydration sachets (ORS)")
                st.write("☐ Personal prescription medicines")

            # ── Emergency Contacts ──
            with st.expander("🆘 Emergency Contacts"):
                st.write("🚔 **Police:** 100 (India) / 911 (USA) / 999 (UK)")
                st.write("🚑 **Ambulance:** 108 (India) / 112 (Europe)")
                st.write("🏥 **Tourist Helpline India:** 1363")
                st.write("🌐 **International SOS:** +65 6338 7800")

            # ── Packing Checklist ──
            with st.expander("🎒 Quick Packing Checklist"):
                st.write("☐ Passport & Visa documents")
                st.write("☐ Travel insurance")
                st.write("☐ Local currency + card")
                st.write("☐ Phone charger & power bank")
                st.write("☐ Basic medicines & first aid")
                st.write("☐ Comfortable walking shoes")
                st.write("☐ Weather appropriate clothing")

        st.divider()

        if st.button("Plan another trip"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
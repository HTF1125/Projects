import streamlit as st
from app.website.static import get_resume, get_profile
from app.website.pages.base import BasePage


class AboutMe(BasePage):
    DESCRIPTION = """
        Results-driven quantitative strategy and financial model developer
        with a strong background in buy-side equity investing.
        Offering 6 years of experience in financial research and strategy
        development, with a focus on developing innovative investment solutions.
        Proficient in quantitative strategy development for institutional clients,
        with 2+ years of experience in delivering successful projects.
    """
    NAME = "RobertHan"
    EMAIL = "hantianfeng@outlook.com"

    def load_page(self):
        st.title(self.NAME)

        cols = st.columns([1, 6])
        with cols[0]:
            st.image(get_profile())
        with cols[1]:
            st.write(self.DESCRIPTION)
            st.write("📫", self.EMAIL)
            st.download_button(
                label=" 📄 Download Resume",
                data=get_resume(),
                file_name="Robert Han.pdf",
                mime="application/octet-stream",
            )
        st.write("\n")
        self.h3("Beliefs")
        self.divider()

        st.markdown(
            """My passion for working in quantitative research stems from my strong belief in
            leveling the playing field in the financial markets. Through the power of data-driven
            analysis and innovative algorithms, I aim to offer institutional-level strategies and
            insights to the average investor. By harnessing the potential of quantitative research,
            I am dedicated to empowering individuals to make well-informed investment decisions and
            navigate the complexities of the market with greater confidence. Contributing to
            democratizing access to sophisticated financial tools motivates me to pursue a career
            in this field, where I can positively impact the financial well-being of a broader
            community."""
        )

        # --- EXPERIENCE & QUALIFICATIONS ---
        st.write("\n")
        self.h3("Experience & Qualifications")
        self.divider()

        col1, col2 = st.columns(2)

        with col1:
            self.h4("Quantitative Strategy")
            st.markdown("- 📈 6 years of experience in developing quant strategies.")
            st.markdown("- 🖥️ Extensive expertise in Python and Excel (VBA).")
            st.markdown("- 📊 Skilled at applying finance and statistics in practioner.")

            self.h4("Team Collaboration")
            st.markdown("- 🤝 Team player, fostering collaboration & communication.")
            st.markdown("- 🚀 Initiative, ownership.")
            st.markdown("- 🎯 Goal-oriented mindset, working towards team objectives.")
        with col2:
            self.h4("Hard Skills")
            st.markdown("- 💻 Programming: Python, SQL, VBA")
            st.markdown("- 📚 Modeling: Portfolio Optimization, Factor & Risk Premia")
            st.markdown("- 🌍 Languages: Chinese, English, Korean, Japanese(Beginner)")

            self.h4("Additional Skills")
            st.markdown("- 🔍 Advanced knowledge of data analysis and visualization.")
            st.markdown("- 🏆 Proven track record of delivering high-quality results.")
            st.markdown("- 📖 Continuously keeping up with the latest trends.")

        # --- WORK HISTORY ---
        st.write("\n")
        self.h3("Work History")
        self.divider()

        # --- JOB 1 ---
        self.h4("🚧 Asset Allocation Strategist | HeungKuk Life Insurace")
        st.markdown("08/2023 - Present | ")
        st.write(
            """
            -► Long-Term Capital Market Assumtpions [Building Block Method].
            -► Strategical Asset Allocation for General Insurance Account.
            """
        )
        self.divider()

        self.h4("🚧 Quantitative Strategist | Dneuro Inc.")
        st.markdown("05/2021 - 05/2023 | 2 Years 0 Months")
        st.write(
            """
            -► Spearheaded the development of a comprehensive Robo-Advisor project,
              encompassing all aspects of wealth management, including goal-based
              dynamic asset allocation, market regime analysis, macro factors, and
              asset selection methodologies. Integrated behavioral finance to
              enhance client experience.

            -► Led the US equity factor library construction project, developing
              Python calculations for over 100 fundamental factors. Implemented a
              database operations module using MariaDB to facilitate efficient
              data management.

            -► Provided consulting services for OCIO Strategic Asset Allocation,
              utilizing simulations and portfolio optimization techniques.
              Developed a user-friendly web portal for client interactions and
              customized asset allocation strategies.
            """
        )

        self.divider()

        # --- JOB 2 ---
        self.h4("🚧 Global Solutions Specialist | Woori Asset Management Corp.")
        st.markdown("03/2017 - 05/2021 | 4 Years 2 Months")
        st.write(
            """
            -► Contributed to quantitative research and played a key role in
              developing models for optimizing global multi-asset portfolios.
              Leveraged advanced quantitative techniques to analyze market data,
              identify trends, and enhance portfolio performance and risk management.

            -► Conducted global research, focusing on US and Chinese equities.
              Built multiple financial analysis models in Excel (VBA) using
              Bloomberg and Wind terminals.

            -► Managed liquidity positions for all global equity funds, ensuring
              efficient execution of Forex hedges using futures and forward
              contracts. Monitored market conditions and implemented hedging
              strategies to mitigate currency risks and optimize fund performance.
            """
        )

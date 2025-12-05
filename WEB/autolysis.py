import os
import json
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage # For basic image ops

# For Search Engine API (example with a placeholder, replace with actual API client)
# import googleapiclient.discovery # If using Google Custom Search
# import serpapi # If using SerpApi

# For Gemini API (assuming you have google-generativeai installed)
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (for API keys)
load_dotenv()

class DataAgentConfig:
    """Manages configuration settings."""
    def __init__(self):
        self.SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "YOUR_SEARCH_API_KEY")
        self.SEARCH_ENGINE_CX = os.getenv("SEARCH_ENGINE_CX", "YOUR_SEARCH_ENGINE_CX") # For Google Custom Search
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
        self.DATA_STORAGE_DIR = "collected_data"
        self.REPORT_OUTPUT_DIR = "reports"
        self.MAX_FETCH_ITERATIONS = 5
        self.FETCH_DELAY_SECONDS = 5 # To avoid rate limiting
        self.INITIAL_QUERIES = [
            "future of AI in healthcare",
            "impact of quantum computing on finance",
            "sustainable energy solutions 2025"
        ]
        # Ensure directories exist
        os.makedirs(self.DATA_STORAGE_DIR, exist_ok=True)
        os.makedirs(self.REPORT_OUTPUT_DIR, exist_ok=True)

class DataStorageManager:
    """Handles storing and retrieving data (simplified using JSON files for now).
       In a real system, this would be a database wrapper (e.g., SQLite, PostgreSQL)."""
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def _get_filepath(self, query_id, type_):
        return os.path.join(self.base_dir, f"{query_id}_{type_}.json")

    def store_raw_search_results(self, query_id, results):
        filepath = self._get_filepath(query_id, "search_results")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Stored search results for {query_id}")

    def store_web_page_content(self, url_hash, content):
        filepath = os.path.join(self.base_dir, f"web_content_{url_hash}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Stored web content for {url_hash}")

    def store_gemini_analysis(self, query_id, analysis_data):
        filepath = self._get_filepath(query_id, "gemini_analysis")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=4)
        print(f"Stored Gemini analysis for {query_id}")

    def store_processed_data(self, query_id, df):
        filepath = os.path.join(self.base_dir, f"{query_id}_processed_data.csv")
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Stored processed data for {query_id}")

    # Add methods to retrieve data as needed

class SearchEngineFetcher:
    """Fetches data from a search engine API."""
    def __init__(self, api_key, cx=None):
        self.api_key = api_key
        self.cx = cx # Custom Search Engine ID
        # Initialize Gemini for potential query refinement
        genai.configure(api_key=DataAgentConfig().GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-pro')

    def fetch_results(self, query, num_results=10):
        """
        Fetches search results. This is a placeholder; you'd integrate with a
        specific search API like Google Custom Search, SerpApi, or Brave Search.
        """
        print(f"Fetching search results for: '{query}'")
        # --- Placeholder for actual API call ---
        # Example using requests for a hypothetical API
        # Actual implementation would use the specific library for the chosen API
        try:
            # Example using Google Custom Search API (requires google-api-python-client)
            # from googleapiclient.discovery import build
            # service = build("customsearch", "v1", developerKey=self.api_key)
            # res = service.cse().list(q=query, cx=self.cx, num=num_results).execute()
            # return res.get('items', [])

            # For a simpler, mock response:
            mock_results = [
                {"title": f"Title for {query} - {i}", "link": f"https://example.com/page{i}-{query.replace(' ', '-')}", "snippet": f"Snippet related to {query} for result {i}."},
                {"title": f"Another Title for {query} - {i+1}", "link": f"https://example.org/doc{i+1}-{query.replace(' ', '-')}", "snippet": f"More info on {query} for result {i+1}."}
            ]
            # Simulate a real API call delay
            time.sleep(1)
            return mock_results
        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []

    def refine_query_with_gemini(self, current_query, context=""):
        """Uses Gemini to refine search queries based on current understanding."""
        prompt = f"Given the current search query '{current_query}' and context '{context}', suggest a more precise or related search query that could uncover deeper insights. Just provide the refined query, no explanations."
        try:
            response = self.gemini_model.generate_content(prompt)
            refined_query = response.text.strip()
            print(f"Gemini refined query from '{current_query}' to '{refined_query}'")
            return refined_query if refined_query else current_query
        except Exception as e:
            print(f"Error refining query with Gemini: {e}")
            return current_query

class WebScraper:
    """Fetches and parses content from web pages."""
    def fetch_page_content(self, url):
        print(f"Fetching content from: {url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract main content (e.g., paragraphs, headings, lists)
            main_content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
            text_content = "\n".join([tag.get_text(separator=' ', strip=True) for tag in main_content_tags])
            return text_content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            return None

class GeminiAnalyzer:
    """Uses Gemini API for text analysis and summarization."""
    def __init__(self):
        genai.configure(api_key=DataAgentConfig().GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def summarize_text(self, text, max_words=150):
        if not text.strip():
            return "No content to summarize."
        prompt = f"Summarize the following text concisely, focusing on key insights and findings, in about {max_words} words:\n\n{text}"
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error summarizing text with Gemini: {e}")
            return f"Error in summarization: {e}"

    def extract_keywords(self, text, num_keywords=10):
        if not text.strip():
            return []
        prompt = f"Extract the top {num_keywords} most important keywords or phrases from the following text, comma-separated:\n\n{text}"
        try:
            response = self.model.generate_content(prompt)
            return [kw.strip() for kw in response.text.strip().split(',') if kw.strip()]
        except Exception as e:
            print(f"Error extracting keywords with Gemini: {e}")
            return []

    def perform_sentiment_analysis(self, text):
        if not text.strip():
            return "Neutral"
        prompt = f"Analyze the sentiment of the following text (Positive, Negative, Neutral). Just provide the sentiment, no explanations:\n\n{text}"
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error performing sentiment analysis with Gemini: {e}")
            return "Unknown"

    def identify_trends_and_patterns(self, text_list):
        if not text_list:
            return "No text data to analyze for trends."
        combined_text = "\n\n---\n\n".join(text_list)
        prompt = f"Analyze the following collection of texts and identify any emerging trends, common themes, or significant patterns. Provide a concise summary of your findings:\n\n{combined_text}"
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error identifying trends with Gemini: {e}")
            return f"Error in trend analysis: {e}"

class DataAnalyzerAndPresenter:
    """Analyzes processed data and generates various output forms."""
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()

    def analyze_and_present(self, query_id, processed_df, analyses_text_data):
        print(f"Analyzing and presenting data for {query_id}...")

        # 1. Generate Basic Report (PDF)
        self._generate_pdf_report(query_id, processed_df, analyses_text_data)

        # 2. Generate Data Sheet (Excel/CSV)
        self._generate_data_sheet(query_id, processed_df)

        # 3. Generate Graphs (PNG)
        self._generate_graphs(query_id, processed_df)

        # 4. (Conceptual) Image processing/Embedding
        # For actual image processing, you'd need a source of images and logic to process them.
        # This is a placeholder for how you might integrate it.
        # self._handle_images(query_id)

        print(f"Analysis and presentation complete for {query_id}.")

    def _generate_pdf_report(self, query_id, df, analyses_text_data):
        doc_path = os.path.join(self.output_dir, f"{query_id}_report.pdf")
        doc = SimpleDocTemplate(doc_path, pagesize=letter)
        story = []

        story.append(Paragraph(f"<b>Research Report: {query_id.replace('_', ' ').title()}</b>", self.styles['h1']))
        story.append(Spacer(1, 0.2 * 10))

        story.append(Paragraph("<h3>Summary of Findings from Gemini Analysis:</h3>", self.styles['h3']))
        story.append(Paragraph(analyses_text_data.get('overall_trend_analysis', 'N/A'), self.styles['Normal']))
        story.append(Spacer(1, 0.2 * 10))

        story.append(Paragraph("<h3>Top Keywords Identified:</h3>", self.styles['h3']))
        keywords = analyses_text_data.get('keywords', [])
        if keywords:
            story.append(Paragraph(", ".join(keywords), self.styles['Normal']))
        else:
            story.append(Paragraph("No keywords identified.", self.styles['Normal']))
        story.append(Spacer(1, 0.2 * 10))


        # Add a table from the DataFrame (basic representation)
        if not df.empty:
            story.append(Paragraph("<h3>Raw Data Snippet:</h3>", self.styles['h3']))
            # Convert DataFrame to a string representation or use reportlab.platypus.Table
            story.append(Paragraph(df.head().to_string(), self.styles['Code']))
            story.append(Spacer(1, 0.2 * 10))

        doc.build(story)
        print(f"Generated PDF report: {doc_path}")

    def _generate_data_sheet(self, query_id, df):
        excel_path = os.path.join(self.output_dir, f"{query_id}_data.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"Generated Excel data sheet: {excel_path}")

    def _generate_graphs(self, query_id, df):
        # This is highly dependent on the type of data collected.
        # For demonstration, let's imagine we collected some numerical data (e.g., "mentions_count")
        # You'd need to adapt this based on your actual data schema.

        # Create a dummy count for demonstration
        if 'source' in df.columns:
            source_counts = df['source'].value_counts()
            if not source_counts.empty:
                plt.figure(figsize=(10, 6))
                sns.barplot(x=source_counts.index, y=source_counts.values)
                plt.title(f'Number of Mentions by Source for {query_id.replace("_", " ").title()}')
                plt.xlabel('Source')
                plt.ylabel('Count')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                graph_path = os.path.join(self.output_dir, f"{query_id}_source_mentions.png")
                plt.savefig(graph_path)
                plt.close()
                print(f"Generated source mentions graph: {graph_path}")

        # Example: Sentiment distribution (if sentiment analysis was applied to each snippet)
        if 'sentiment' in df.columns and not df['sentiment'].empty:
            sentiment_counts = df['sentiment'].value_counts()
            if not sentiment_counts.empty:
                plt.figure(figsize=(8, 8))
                plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
                plt.title(f'Sentiment Distribution for {query_id.replace("_", " ").title()}')
                plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
                sentiment_graph_path = os.path.join(self.output_dir, f"{query_id}_sentiment_distribution.png")
                plt.savefig(sentiment_graph_path)
                plt.close()
                print(f"Generated sentiment distribution graph: {sentiment_graph_path}")


    def _handle_images(self, query_id):
        # This is a highly conceptual placeholder.
        # If your search API returned image URLs, you'd fetch them,
        # potentially process (e.g., resize, add watermark), and embed in reports.
        # For now, it just demonstrates the intent.
        dummy_image_path = os.path.join(self.output_dir, "dummy_image.png")
        if not os.path.exists(dummy_image_path):
            # Create a simple dummy image for demonstration
            img = PILImage.new('RGB', (60, 30), color = 'red')
            img.save(dummy_image_path)
        print(f"Placeholder for image handling for {query_id}.")
        # To embed in PDF:
        # story.append(RLImage(dummy_image_path, width=100, height=50))


class ResearchAgent:
    """The main orchestration agent."""
    def __init__(self):
        self.config = DataAgentConfig()
        self.storage = DataStorageManager(self.config.DATA_STORAGE_DIR)
        self.search_fetcher = SearchEngineFetcher(self.config.SEARCH_API_KEY, self.config.SEARCH_ENGINE_CX)
        self.web_scraper = WebScraper()
        self.gemini_analyzer = GeminiAnalyzer()
        self.data_presenter = DataAnalyzerAndPresenter(self.config.REPORT_OUTPUT_DIR)
        self.processed_data_store = {} # Temporary store for current iteration's processed data

    def run(self):
        current_queries = list(self.config.INITIAL_QUERIES) # Copy to allow modification
        iteration = 0

        while iteration < self.config.MAX_FETCH_ITERATIONS and current_queries:
            query = current_queries.pop(0) # Get the next query
            query_id = query.replace(" ", "_").lower() # Simple ID for storage

            print(f"\n--- Iteration {iteration + 1}: Processing query '{query}' ---")

            # Phase 1: Fetch from Search Engine API
            search_results = self.search_fetcher.fetch_results(query)
            self.storage.store_raw_search_results(query_id, search_results)

            # Phase 2: Web Scraping and Initial Processing
            collected_web_content = []
            if search_results:
                for i, result in enumerate(search_results):
                    if 'link' in result:
                        url = result['link']
                        # Simple hash for URL to filename
                        url_hash = str(abs(hash(url)))[:10]
                        content = self.web_scraper.fetch_page_content(url)
                        if content:
                            self.storage.store_web_page_content(url_hash, content)
                            collected_web_content.append({
                                'query_id': query_id,
                                'source': url,
                                'title': result.get('title', 'N/A'),
                                'snippet': result.get('snippet', 'N/A'),
                                'full_content': content
                            })
                            # Limit number of pages scraped per query to avoid overwhelming
                            if i >= 2: # Scrape first 3 links
                                break
                    time.sleep(self.config.FETCH_DELAY_SECONDS / 2) # Shorter delay for pages

            # Convert collected content to DataFrame for structured processing
            processed_df = pd.DataFrame(collected_web_content)

            # Phase 3: Gemini Analysis
            gemini_analysis_results = {}
            if not processed_df.empty:
                # Summarize snippets/full content using Gemini
                processed_df['gemini_summary'] = processed_df['full_content'].apply(
                    lambda x: self.gemini_analyzer.summarize_text(x, max_words=100) if pd.notna(x) else "No content"
                )

                # Perform sentiment analysis
                processed_df['sentiment'] = processed_df['full_content'].apply(
                    lambda x: self.gemini_analyzer.perform_sentiment_analysis(x) if pd.notna(x) else "Unknown"
                )

                # Extract keywords from combined content
                all_content_text = " ".join(processed_df['full_content'].dropna().tolist())
                gemini_analysis_results['keywords'] = self.gemini_analyzer.extract_keywords(all_content_text, num_keywords=15)

                # Identify overall trends
                all_summaries_text = " ".join(processed_df['gemini_summary'].dropna().tolist())
                gemini_analysis_results['overall_trend_analysis'] = self.gemini_analyzer.identify_trends_and_patterns(
                    processed_df['gemini_summary'].dropna().tolist()
                )
            else:
                gemini_analysis_results['keywords'] = []
                gemini_analysis_results['overall_trend_analysis'] = "No content collected for trend analysis."

            self.storage.store_gemini_analysis(query_id, gemini_analysis_results)
            self.storage.store_processed_data(query_id, processed_df)
            self.processed_data_store[query_id] = {'df': processed_df, 'analysis': gemini_analysis_results}


            # Phase 4: Iterate/Refine (e.g., use Gemini to suggest new queries)
            if iteration < self.config.MAX_FETCH_ITERATIONS - 1:
                # Use analysis insights to refine next query or add new queries
                # For simplicity, let's just refine the current query
                if gemini_analysis_results['overall_trend_analysis'] and gemini_analysis_results['overall_trend_analysis'] != "No content collected for trend analysis.":
                     new_suggested_query = self.search_fetcher.refine_query_with_gemini(
                         query, context=gemini_analysis_results['overall_trend_analysis']
                     )
                     if new_suggested_query and new_suggested_query != query and new_suggested_query not in current_queries:
                         current_queries.append(new_suggested_query)
                         print(f"Added refined query for next iteration: '{new_suggested_query}'")


            iteration += 1
            time.sleep(self.config.FETCH_DELAY_SECONDS) # Respect API rate limits

        print("\n--- All Fetching Iterations Complete ---")

        # Phase 5: Final Analysis and Presentation of All Collected Data
        print("\n--- Generating Final Reports and Visualizations ---")
        for q_id, data in self.processed_data_store.items():
            self.data_presenter.analyze_and_present(q_id, data['df'], data['analysis'])
        print("All reports generated.")


# --- Main Execution ---
if __name__ == "__main__":
    # IMPORTANT: Set your API keys as environment variables or directly in DataAgentConfig
    # For example, in your shell before running:
    # export SEARCH_API_KEY="your_actual_search_api_key"
    # export SEARCH_ENGINE_CX="your_custom_search_engine_id" # If using Google Custom Search
    # export GEMINI_API_KEY="your_actual_gemini_api_key"

    # Or create a .env file in the same directory:
    # SEARCH_API_KEY="your_actual_search_api_key"
    # SEARCH_ENGINE_CX="your_custom_search_engine_id"
    # GEMINI_API_KEY="your_actual_gemini_api_key"
    # Then ensure `pip install python-dotenv` is done

    # Install required libraries:
    # pip install requests beautifulsoup4 pandas matplotlib seaborn reportlab Pillow google-generativeai python-dotenv

    agent = ResearchAgent()
    agent.run()
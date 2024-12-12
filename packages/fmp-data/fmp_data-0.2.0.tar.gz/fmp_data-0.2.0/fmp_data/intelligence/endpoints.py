from fmp_data.intelligence.models import (
    AnalystEstimate,
    AnalystRecommendation,
    CrowdfundingOffering,
    CryptoNewsArticle,
    DividendEvent,
    EarningConfirmed,
    EarningEvent,
    EarningSurprise,
    EquityOffering,
    EquityOfferingSearchItem,
    ESGBenchmark,
    ESGData,
    ESGRating,
    FMPArticlesResponse,
    ForexNewsArticle,
    GeneralNewsArticle,
    HistoricalSocialSentiment,
    HouseDisclosure,
    IPOEvent,
    PressRelease,
    PressReleaseBySymbol,
    PriceTarget,
    PriceTargetConsensus,
    PriceTargetSummary,
    SenateTrade,
    SocialSentimentChanges,
    StockNewsArticle,
    StockNewsSentiment,
    StockSplitEvent,
    TrendingSocialSentiment,
    UpgradeDowngrade,
    UpgradeDowngradeConsensus,
)
from fmp_data.models import (
    APIVersion,
    Endpoint,
    EndpointParam,
    HTTPMethod,
    ParamLocation,
    ParamType,
    URLType,
)

PRICE_TARGET = Endpoint(
    name="price_target",
    path="price-target",
    version=APIVersion.V4,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get price targets",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=PriceTarget,
)

PRICE_TARGET_SUMMARY = Endpoint(
    name="price_target_summary",
    path="price-target-summary",
    version=APIVersion.V4,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get price target summary",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=PriceTargetSummary,
)

PRICE_TARGET_CONSENSUS = Endpoint(
    name="price_target_consensus",
    path="price-target-consensus",
    version=APIVersion.V4,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get price target consensus",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=PriceTargetConsensus,
)

ANALYST_ESTIMATES = Endpoint(
    name="analyst_estimates",
    path="analyst-estimates/{symbol}",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get analyst estimates",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.PATH,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=AnalystEstimate,
)

ANALYST_RECOMMENDATIONS = Endpoint(
    name="analyst_recommendations",
    path="analyst-stock-recommendations/{symbol}",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get analyst recommendations",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.PATH,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=AnalystRecommendation,
)

UPGRADES_DOWNGRADES = Endpoint(
    name="upgrades_downgrades",
    path="upgrades-downgrades",
    version=APIVersion.V4,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get upgrades and downgrades",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=UpgradeDowngrade,
)

UPGRADES_DOWNGRADES_CONSENSUS = Endpoint(
    name="upgrades_downgrades_consensus",
    path="upgrades-downgrades-consensus",
    version=APIVersion.V4,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get upgrades and downgrades consensus",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=UpgradeDowngradeConsensus,
)

EARNINGS_CALENDAR = Endpoint(
    name="earnings_calendar",
    path="earning_calendar",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get earnings calendar",
    mandatory_params=[],
    optional_params=[
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
    ],
    response_model=EarningEvent,
)

EARNINGS_CONFIRMED = Endpoint(
    name="earnings_confirmed",
    path="earning-calendar-confirmed",
    version=APIVersion.V4,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get confirmed earnings dates",
    mandatory_params=[],
    optional_params=[
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
    ],
    response_model=EarningConfirmed,
)

EARNINGS_SURPRISES = Endpoint(
    name="earnings_surprises",
    path="earnings-surprises/{symbol}",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get earnings surprises",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.PATH,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=EarningSurprise,
)

HISTORICAL_EARNINGS = Endpoint(
    name="historical_earnings",
    path="historical/earning_calendar/{symbol}",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get historical earnings",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.PATH,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=EarningEvent,
)

DIVIDENDS_CALENDAR = Endpoint(
    name="dividends_calendar",
    path="stock_dividend_calendar",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get dividends calendar",
    mandatory_params=[],
    optional_params=[
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
    ],
    response_model=DividendEvent,
)

STOCK_SPLITS_CALENDAR = Endpoint(
    name="stock_splits_calendar",
    path="stock_split_calendar",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get stock splits calendar",
    mandatory_params=[],
    optional_params=[
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
    ],
    response_model=StockSplitEvent,
)

IPO_CALENDAR = Endpoint(
    name="ipo_calendar",
    path="ipo_calendar",
    version=APIVersion.V3,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get IPO calendar",
    mandatory_params=[],
    optional_params=[
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
    ],
    response_model=IPOEvent,
)

FMP_ARTICLES_ENDPOINT = Endpoint(
    name="fmp_articles",
    path="fmp/articles",
    version=APIVersion.V3,
    description="Get a list of the latest FMP articles",
    mandatory_params=[],
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
        EndpointParam(
            name="size",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Number of articles per page",
        ),
    ],
    response_model=FMPArticlesResponse,
)

GENERAL_NEWS_ENDPOINT = Endpoint(
    name="general_news",
    path="general_news",
    version=APIVersion.V4,
    description="Get a list of the latest general news articles",
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
    ],
    mandatory_params=[],
    response_model=GeneralNewsArticle,
)

STOCK_NEWS_ENDPOINT = Endpoint(
    name="stock_news",
    path="stock_news",
    version=APIVersion.V3,
    description="Get a list of the latest stock news articles",
    optional_params=[
        EndpointParam(
            name="tickers",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Comma-separated list of stock tickers",
        ),
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=True,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=True,
            description="End date",
        ),
        EndpointParam(
            name="limit",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=False,
            description="Maximum number of articles to return",
        ),
    ],
    mandatory_params=[],
    response_model=StockNewsArticle,
)

STOCK_NEWS_SENTIMENTS_ENDPOINT = Endpoint(
    name="stock_news_sentiments",
    path="stock-news-sentiments-rss-feed",
    version=APIVersion.V4,
    description="Get a list of the latest stock news articles with sentiment analysis",
    mandatory_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
    ],
    optional_params=[],
    response_model=StockNewsSentiment,
)

FOREX_NEWS_ENDPOINT = Endpoint(
    name="forex_news",
    path="forex_news",
    version=APIVersion.V4,
    description="Get a list of the latest forex news articles",
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=False,
            description="Forex symbol",
        ),
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
        EndpointParam(
            name="limit",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=False,
            description="Maximum number of articles to return",
        ),
    ],
    mandatory_params=[],
    response_model=ForexNewsArticle,
)

CRYPTO_NEWS_ENDPOINT = Endpoint(
    name="crypto_news",
    path="crypto_news",
    version=APIVersion.V4,
    description="Get a list of the latest crypto news articles",
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Crypto symbol",
        ),
        EndpointParam(
            name="from",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
        ),
        EndpointParam(
            name="to",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
        ),
        EndpointParam(
            name="limit",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=False,
            description="Maximum number of articles to return",
        ),
    ],
    mandatory_params=[],
    response_model=CryptoNewsArticle,
)

PRESS_RELEASES_ENDPOINT = Endpoint(
    name="press_releases",
    path="press-releases",
    version=APIVersion.V3,
    description="Get a list of the latest press releases",
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
    ],
    mandatory_params=[],
    response_model=PressRelease,
)

PRESS_RELEASES_BY_SYMBOL_ENDPOINT = Endpoint(
    name="press_releases_by_symbol",
    path="press-releases/{symbol}",
    version=APIVersion.V3,
    description="Get a list of the latest press releases for a specific company",
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=False,
            default=0,
            description="Page number",
        ),
    ],
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.PATH,
            param_type=ParamType.STRING,
            required=True,
            description="Company symbol",
        )
    ],
    response_model=PressReleaseBySymbol,
)

HISTORICAL_SOCIAL_SENTIMENT_ENDPOINT = Endpoint(
    name="historical_social_sentiment",
    path="historical/social-sentiment",
    version=APIVersion.V4,
    description="Get historical social sentiment data",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
        ),
    ],
    response_model=HistoricalSocialSentiment,
)

TRENDING_SOCIAL_SENTIMENT_ENDPOINT = Endpoint(
    name="trending_social_sentiment",
    path="social-sentiments/trending",
    version=APIVersion.V4,
    description="Get trending social sentiment data",
    mandatory_params=[
        EndpointParam(
            name="type",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Sentiment type (bullish, bearish)",
        ),
        EndpointParam(
            name="source",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Sentiment source (stocktwits)",
        ),
    ],
    optional_params=[],
    response_model=TrendingSocialSentiment,
)

SOCIAL_SENTIMENT_CHANGES_ENDPOINT = Endpoint(
    name="social_sentiment_changes",
    path="social-sentiments/change",
    version=APIVersion.V4,
    description="Get changes in social sentiment data",
    mandatory_params=[
        EndpointParam(
            name="type",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Sentiment type (bullish, bearish)",
        ),
        EndpointParam(
            name="source",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Sentiment source (stocktwits)",
        ),
    ],
    optional_params=[],
    response_model=SocialSentimentChanges,
)

# ESG Endpoints
ESG_DATA = Endpoint(
    name="esg_data",
    path="esg-environmental-social-governance-data",
    version=APIVersion.V4,
    description="Get ESG data for a company",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Company symbol",
        )
    ],
    optional_params=[],
    response_model=ESGData,
)

ESG_RATINGS = Endpoint(
    name="esg_ratings",
    path="esg-environmental-social-governance-data-ratings",
    version=APIVersion.V4,
    description="Get ESG ratings for a company",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Company symbol",
        )
    ],
    optional_params=[],
    response_model=ESGRating,
)

ESG_BENCHMARK = Endpoint(
    name="esg_benchmark",
    path="esg-environmental-social-governance-sector-benchmark",
    version=APIVersion.V4,
    description="Get ESG sector benchmark data",
    mandatory_params=[
        EndpointParam(
            name="year",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Benchmark year",
        )
    ],
    optional_params=[],
    response_model=ESGBenchmark,
)

# Government Trading Endpoints
SENATE_TRADING = Endpoint(
    name="senate_trading",
    path="senate-trading",
    version=APIVersion.V4,
    description="Get Senate trading data",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=SenateTrade,
)

SENATE_TRADING_RSS = Endpoint(
    name="senate_trading_rss",
    path="senate-trading-rss-feed",
    version=APIVersion.V4,
    description="Get Senate trading RSS feed",
    mandatory_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
            default=0,
        )
    ],
    optional_params=[],
    response_model=SenateTrade,
)

HOUSE_DISCLOSURE = Endpoint(
    name="house_disclosure",
    path="senate-disclosure",
    version=APIVersion.V4,
    description="Get House disclosure data",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Stock symbol",
        )
    ],
    optional_params=[],
    response_model=HouseDisclosure,
)

HOUSE_DISCLOSURE_RSS = Endpoint(
    name="house_disclosure_rss",
    path="senate-disclosure-rss-feed",
    version=APIVersion.V4,
    description="Get House disclosure RSS feed",
    mandatory_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
            default=0,
        )
    ],
    optional_params=[],
    response_model=HouseDisclosure,
)

# Fundraising Endpoints
CROWDFUNDING_RSS = Endpoint(
    name="crowdfunding_rss",
    path="crowdfunding-offerings-rss-feed",
    version=APIVersion.V4,
    description="Get crowdfunding offerings RSS feed",
    mandatory_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
            default=0,
        )
    ],
    optional_params=[],
    response_model=CrowdfundingOffering,
)

CROWDFUNDING_SEARCH = Endpoint(
    name="crowdfunding_search",
    path="crowdfunding-offerings/search",
    version=APIVersion.V4,
    description="Search crowdfunding offerings",
    mandatory_params=[
        EndpointParam(
            name="name",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Company or offering name",
        )
    ],
    optional_params=[],
    response_model=CrowdfundingOffering,
)

CROWDFUNDING_BY_CIK = Endpoint(
    name="crowdfunding_by_cik",
    path="crowdfunding-offerings",
    version=APIVersion.V4,
    description="Get crowdfunding offerings by CIK",
    mandatory_params=[
        EndpointParam(
            name="cik",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Company CIK number",
        )
    ],
    optional_params=[],
    response_model=CrowdfundingOffering,
)

EQUITY_OFFERING_RSS = Endpoint(
    name="equity_offering_rss",
    path="fundraising-rss-feed",
    version=APIVersion.V4,
    description="Get equity offering RSS feed",
    mandatory_params=[
        EndpointParam(
            name="page",
            location=ParamLocation.QUERY,
            param_type=ParamType.INTEGER,
            required=True,
            description="Page number",
            default=0,
        )
    ],
    optional_params=[],
    response_model=EquityOffering,
)

EQUITY_OFFERING_SEARCH = Endpoint(
    name="equity_offering_search",
    path="fundraising/search",
    version=APIVersion.V4,
    description="Search equity offerings",
    mandatory_params=[
        EndpointParam(
            name="name",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Company or offering name",
        )
    ],
    optional_params=[],
    response_model=EquityOfferingSearchItem,
)

EQUITY_OFFERING_BY_CIK = Endpoint(
    name="equity_offering_by_cik",
    path="fundraising",
    version=APIVersion.V4,
    description="Get equity offerings by CIK",
    mandatory_params=[
        EndpointParam(
            name="cik",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Company CIK number",
        )
    ],
    optional_params=[],
    response_model=EquityOffering,
)

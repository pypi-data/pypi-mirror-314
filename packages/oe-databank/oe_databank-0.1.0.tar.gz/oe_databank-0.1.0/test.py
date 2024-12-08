import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from oe_databank.enums import FileFormat, Frequency, ListingType, Order, SelectionSortOrder, SelectionType, Sequence
from oe_databank.models import DownloadRequestRegion, DownloadRequestVariable, FileDownloadRequestDto, Selection

load_dotenv(Path.home() / ".local/oe.env")

from oe_databank import DatabankAsyncClient



async def main():
    client = DatabankAsyncClient(api_key=os.environ["OE_DATA_API_KEY"])
    print("Fetching data...")
    # await asyncio.gather(
    #     client.list_databanks(to_path="databanks.json"),
    #     client.get_tree("Indicators_GCT", to_path="tree.json"),
    #     client.get_regions("GCT", to_path="regions.json"),
    # )

    await client.query(
        request=FileDownloadRequestDto(
            selections=[
                Selection(
                    selectionType=SelectionType.QUERY,
                    isTemporarySelection=True,
                    databankCode="GCT",
                    sequence=Sequence.EARLIEST_TO_LATEST,
                    groupingMode=False,
                    transposeColumns=False,
                    order=Order.LOCATION_INDICATOR,
                    indicatorSortOrder=SelectionSortOrder.ALPHABETICAL,
                    locationSortOrder=SelectionSortOrder.ALPHABETICAL,
                    format=0,
                    legacyDatafeedFileStructure=False,
                    variables=[
                        DownloadRequestVariable(
                            variableCode="MRSA!$",
                            productTypeCode="GCT",
                            measureCodes=[],
                        )
                    ],
                    regions=[
                        DownloadRequestRegion(
                            databankCode="GCT",
                            regionCode="ETH_ADD",
                        ),
                    ],
                    listingType=ListingType.SHARED,
                    isDataFeed=False,
                    startYear=2000,
                    endYear=2001,
                    precision=5,
                    frequency=Frequency.BOTH,
                    stackedQuarters=False,
                )
            ],
            format=FileFormat.CSV,
        ),
        to_path="data.csv",
    )


asyncio.run(main())

import asyncio
from datetime import timedelta

import mlflow.sklearn
import pandas as pd
from mlflow.pyfunc import PyFuncModel

from kelvin.ai import RollingWindow
from kelvin.application import KelvinApp, filters
from kelvin.krn import KRNAsset
from kelvin.message import Recommendation


async def run_model(app: KelvinApp, asset: str, df: pd.DataFrame, model: PyFuncModel) -> None:
    # Print data frame
    print(f"Asset: {asset}\n\n{df}\n\n")

    # Clean up df by dropping rows with missing values
    df = df.dropna()

    if not df.empty:
        try:
            # Perform prediction using the loaded model
            prediction = model.predict(df)

            print(f"Prediction: {prediction}")

            # Create and Publish a Recommendation
            await app.publish(
                Recommendation(
                    resource=KRNAsset(asset),
                    type="prediction",
                    expiration_date=timedelta(hours=1),
                    description=f"Model has predicted the following value: {prediction}",
                    control_changes=[],
                )
            )

        except Exception as e:
            print(f"Error during prediction: {str(e)}")


async def main() -> None:
    # Load the MLflow model
    model = mlflow.pyfunc.load_model("model")
    print("Model successfully loaded")

    # Creating instance of Kelvin App Client
    app = KelvinApp()

    # Connect the App Client
    await app.connect()

    print("App connected successfully")

    # Subscribe to the asset data streams
    stream = app.stream_filter(filters.is_asset_data_message)

    # Create a rolling window
    rolling_window = RollingWindow(
        datastreams=[i.name for i in app.inputs],  # App inputs
        max_window_duration=300,  # max of 5 minutes of data
        max_data_points=10,  # max of 10 data points
        timestamp_rounding_interval=timedelta(seconds=30),  # round to the nearest 30 seconds
    )

    async for msg in stream:
        # Add the message to the rolling window
        rolling_window.append(msg)

        # Run model
        await run_model(
            app=app, asset=msg.resource.asset, df=rolling_window.get_asset_df(msg.resource.asset), model=model
        )


if __name__ == "__main__":
    asyncio.run(main())

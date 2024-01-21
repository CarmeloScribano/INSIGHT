
from ingestor import get_data_frame
from utils import get_trades_by_type, get_duration_of_x_and_y

df = get_data_frame("Exchange_1")
ack_order_duration_df = get_duration_of_x_and_y(df=df, msg_x="NewOrderRequest", msg_y="NewOrderAcknowledged")

from website import create_app
"""
from website.daily_data import run_scheduler
from website.all_data import every_month_data
import threading
"""


app = create_app()

if __name__ == '__main__':
   # Start the scheduler thread
    """
    threading.Thread(target=run_scheduler).start()
    threading.Thread(target=every_month_data).start()
    """
    app.run(debug=True)

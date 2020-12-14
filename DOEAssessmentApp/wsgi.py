from runserver import app
from DOEAssessmentApp import manager
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
    manager.run()

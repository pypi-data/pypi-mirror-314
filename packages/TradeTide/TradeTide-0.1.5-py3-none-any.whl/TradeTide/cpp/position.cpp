// Position.h
#include <Python.h>

class Position {
public:
    PyObject* start_date;
    PyObject* market;
    double entry_price, exit_price;

    Position(PyObject* start_date, PyObject* market): start_date(start_date), market(market)
    {
        Py_INCREF(this->start_date);
        Py_INCREF(this->market);
        this->extract_entry_price();
    }

    ~Position() {
        Py_DECREF(this->start_date);
        Py_DECREF(this->market);
    }

    void extract_entry_price() {
        PyDateTime_IMPORT;

        // Assuming 'start_date' is a Python datetime object and 'market' is a DataFrame
        PyObject* pyStrDate = PyObject_Str(start_date);

        // Access the 'loc' attribute of the DataFrame to get the row by date
        PyObject* loc = PyObject_GetAttrString(market, "loc");

        // Use 'loc' to access the row corresponding to 'start_date'
        PyObject* args = PyTuple_Pack(1, pyStrDate);
        PyObject* row = PyObject_CallObject(loc, args);

        Py_DECREF(args);
        if (!row) {
            Py_DECREF(loc);
            Py_DECREF(pyStrDate);
            return; // Handle error
        }

        // Extract the 'close' column value from the row
        PyObject* closeValue = PyObject_GetAttrString(row, "close");
        if (closeValue && PyFloat_Check(closeValue)) {
            entry_price = PyFloat_AsDouble(closeValue);
        } else {
            // Handle case where 'close' is not a float or does not exist
            PyErr_SetString(PyExc_RuntimeError, "The 'close' column is missing or not a float.");
        }

        Py_XDECREF(closeValue);
        Py_DECREF(row);
        Py_DECREF(loc);
        Py_DECREF(pyStrDate);
    }

};

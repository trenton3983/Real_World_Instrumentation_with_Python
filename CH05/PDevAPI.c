/*----------------------------------------------------------------------------*/
/* PDevAPI.c                                                                  */
/*----------------------------------------------------------------------------*/
/* Example API "wrapper" code for a Python extension.                         */
/*                                                                            */
/* IMPORTANT NOTICE!                                                          */
/* This code is NOT intended to be a compilable finished product. It is an    */
/* example only. You can use it as a starting template, but you will need to  */
/* modify it for the actual device API you will be using. Don't expect it to  */
/* even compile as it currently stands.                                       */
/*----------------------------------------------------------------------------*/
/* Example source code for the book "Real-World Instrumentation with Python"  */
/* by J. M. Hughes, published by O'Reilly Media, December 2010,               */
/* ISBN 978-0-596-80956-0.                                                    */
/*----------------------------------------------------------------------------*/
#include    <Python.h>
#include    <stdio.h>
#include    <PDev.h>

static PyObject *OpenDev(PyObject *self, PyObject *args)
{
    int     dev_num;
    int     dev_handle;

    PyArg_ParseTuple(args, "i", &dev_num);
    dev_handle = PDevOpen(dev_num);

    return Py_BuildValue("i", dev_handle);
}

static PyObject *CloseDev(PyObject *self, PyObject *args)
{
    int     dev_handle;
    int     rc;

    PyArg_ParseTuple(args, "i", &dev_handle);
    rc = PDevClose(dev_handle);

    return Py_BuildValue("i", rc);
}

static PyObject *ConfigDev(PyObject *self, PyObject *args)
{
    int     dev_handle;
    char    cfg_str[32];
    int     rc;

    memset((char *) cfg_str, '\0', 32);    /* clear config string */

    PyArg_ParseTuple(args, "is", &dev_handle, cfg_str);
    rc = PDevDIOCfg(dev_handle, cfg_str);

    return Py_BuildValue("i", rc);
}

static PyObject *ConfigRst(PyObject *self, PyObject *args)
{
    int     dev_handle;
    int     rc;

    PyArg_ParseTuple(args, "i", &dev_handle);
    rc = PDevCfgReset(dev_handle);

    return Py_BuildValue("i", rc);
}

static PyObject *ReadPin(PyObject *self, PyObject *args)
{
    int     dev_handle;
    int     in_port;
    int     in_pin;
    int     in_value;

    PyArg_ParseTuple(args, "iii", &dev_handle, &in_port, &in_pin);
    in_value = PDevDIOReadBit(dev_handle, in_port, in_pin);

    return Py_BuildValue("i", in_value);
}

static PyObject *ReadPort(PyObject *self, PyObject *args)
{
    int     dev_handle;
    int     in_port;
    int     in_value;

    PyArg_ParseTuple(args, "iii", &dev_handle, &in_port);
    in_value = PDevDIOReadPort(dev_handle, in_port);

    return Py_BuildValue("i", in_value);
}

static PyObject *WritePin(PyObject *self, PyObject *args)
{
    int     dev_handle;
    int     out_port;
    int     out_pin;
    int     out_value;

    PyArg_ParseTuple(args, "iii", &dev_handle, &out_port, &out_pin, &out_value);
    rc = PDevDIOWriteBit(dev_handle, out_port, out_pin, out_value);

    return Py_BuildValue("i", rc);
}


static PyObject *WritePort(PyObject *self, PyObject *args)
    int     dev_handle;
    int     out_port;
    int     out_value;

    PyArg_ParseTuple(args, "iii", &dev_handle, &out_port, &out_value);
    rc = PDevDIOWritePort(dev_handle, out_port, out_value);

    return Py_BuildValue("i", rc);
}

static PyMethodDef PDevapiMethods[] = {
    {"OpenDevice",      OpenDev,    METH_VARARGS, "Open specific DIO device."},
    {"CloseDevice",     CloseDev,   METH_VARARGS, "Close an open DIO device."},
    {"ConfigOutputs",   ConfigDev,  METH_VARARGS, "Config DIO pins as outputs."},
    {"ConfigReset",     ConfigRst,  METH_VARARGS, "Reset all DIO pins to input mode."},
    {"ReadInputPin",    ReadPin,    METH_VARARGS, "Read a single specific pin."},
    {"ReadInputPort",   ReadPort,   METH_VARARGS, "Read an entire 8-bit port."},
    {"WriteOutputPin",  WritePin,   METH_VARARGS, "Write to a specific pin."},
    {"WriteOutputPort", WritePort,  METH_VARARGS, "Write to an entire port."},
    {NULL, NULL}
};

/*******************************************************************************/
/*  initPDevapi
 *
 *  Initialize this module when loaded by Python. Instantiates the methods table.
 *
 *  No input parameters.
 *
 *  Returns nothing.
 *******************************************************************************/
void initPDevAPI(void)
{
    Py_InitModule("PDevapi", PDevapiMethods);

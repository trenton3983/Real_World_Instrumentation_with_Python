/*----------------------------------------------------------------------------*/
/* PDev.h                                                                     */
/*----------------------------------------------------------------------------*/
/* API for a simple hypothetical discrete digital I/O card                    */
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

typedef int dev_handle;

#define PDEV_OK  1
#define PDEV_ERR 0 

/*
 * Open Device Channel
 *
 * Opens a channel to a particular I/O device. The device is specified
 * by passing its unit number, which is assigned to the device by a
 * setup utility. dev_handle is an int type.
 *
 * Returns:   If dev_handle is > 0 then handle is valid
 *            If dev_handle is = 0 then an error has occurred
 */
dev_handle PDevOpen(int unit_num);

/* Close Device Channel
 * Closes a channel to a particular I/O device. Once a channel is
 * closed it must be explicitly re-opened by using the PDevOpen API
 * function. Closing a channel does not reset the DIO configuration.
 *
 * Returns:   If return is 1 (true) then channel closed OK
 *            If return is = 0 then an error has occurred
 */
int PDevClose(dev_handle handle);

/*
 * Reset Device Configuration
 *
 * Forces the device to perform an internal reset. All
 * configuration is returned to the factory default
 * setting (All DIO is defined as inputs).
 *
 * Returns:   1 (true) if no error occurred
 *            0 (false) if error encountered
 */
int PDevCfgReset(dev_handle handle);

/*
 * Configure Device Discrete I/O
 * 
 * Defines the pins to be assigned as outputs. By default all
 * pins are in the read mode initially, and they must be
 * specifically set to the write mode. All 16 I/O pins are
 * assigned at once. For any pin where the corresponding binary
 * value of the assignment parameter is 1, then the pin will
 * be an output.
 * 
 * Returns:   1 (true) if no error occurred
 *            0 (false) if error encountered
 */ 
int PDevDIOCfg(dev_handle handle, int out_pins);


/*
 *Read Discrete Input Pin
 *
 *Reads the data present on a particular pin. The pin may be
 *either an input or an output. If the pin is an output the
 *value returned will be the value last assigned to the pin.
 *
 *Returns:    The input value for the specified pin, which
 *            will be either 0 or 1. An error is indicated
 *            by a return value of –1.
 */
int PDevDIOReadBit(dev_handle handle, int port, int pin);

/*
 * Read Discrete Input Port
 *
 * Reads the data present on an entire port and returns it as a
 * byte value. The individual pins may be either inputs or outputs.
 * If the pins have been defined as inputs then the value read
 * will be the value last assigned to the pins.
 *
 * Returns:   An integer value representing the input states
 *            of all pins in the specified port. Only the
 *            least significant byte of the return value is
 *            valid. An error is indicated by a return value
 *            of –1.
 */
int PDevDIOReadPort(dev_handle handle, int port);

/*
 * Write Discrete Output Pin
 *
 * Sets a particular pin of a specified port to a value of either
 * 0 (off) or 1 (on, typically +5V). The pin must be defined as
 * an output or the call will return an error code.
 *
 * Returns:   1 (true) if no error occurred
 *            0 (false) if error encountered
 */
int PDevDIOWriteBit(dev_handle handle, int port, int pin, int value);

/*
 * Write Discrete Output Port
 *
 * Sets all of the pins of a specified port to the unsigned value
 * passed in port_value parameter. Only the lower eight bits of the
 * parameter are used. If any pin in the port is configured as an
 * input then an error code will be returned.
 *
 * Returns:   1 (true) if no error occurred
 *            0 (false) if error encountered
 */
int PDevDIOWritePort(dev_handle handle, int port, int value);

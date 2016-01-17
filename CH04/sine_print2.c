/*----------------------------------------------------------------------------*/
/* sine_print2.c                                                               */
/*----------------------------------------------------------------------------*/
/* Print a sideways sine wave pattern using ASCII characters                  */
/*                                                                            */
/* Incorporates #define macro for constants.                                  */
/*                                                                            */
/* Outputs an 80-byte array of ASCII characters (otherwise                    */
/* known as a string) 20 times, each time replacing elements                  */
/* in the array with an asterisk ('*') character to create a                  */
/* sideways plot of a sine function.                                          */
/*                                                                            */
/* To compile:                                                                */
/* $ gcc -o sine_print2 sine_print2.c -lm                                     */
/* $ chmod 755 sine_print2                                                    */
/*                                                                            */
/* To run:                                                                    */
/* $ ./sine_print2                                                            */
/*                                                                            */
/*----------------------------------------------------------------------------*/
/* Example source code for the book "Real-World Instrumentation with Python"  */
/* by J. M. Hughes, published by O'Reilly Media, December 2010,               */
/* ISBN 978-0-596-80956-0.                                                    */
/*----------------------------------------------------------------------------*/

#include <stdio.h>          /* for I/O functions            */
#include <math.h>           /* for the sine function        */
#include <string.h>         /* for the memset function      */

#define MAXLINES    20
#define MAXCHARS    80
#define MAXSTR      (MAXCHARS-1)
#define MIDPNT      ((MAXCHARS/2)-1)
#define SCALEDIV    10

int main()
{
    /* local variable declarations */
    int  i;                 /* loop index counter           */
    int  offset;            /* offset into output string    */
    char sinstr[MAXCHARS];  /* data array                   */

    /* preload entire data array with spaces */
    memset(sinstr, 0x20, MAXCHARS);
    sinstr[MAXSTR] = '\0';  /* append string terminator     */

    /* print MAXLINES lines to cover one cycle */
    for(i = 0; i < MAXLINES; i++) {
        offset = MIDPNT + (int)(MIDPNT * sin(M_PI * (float) i/SCALEDIV));

        sinstr[offset] = '*';
        printf("%s\n", sinstr);
        /* print done, clear the character */
        sinstr[offset] = ' ';
    }
}

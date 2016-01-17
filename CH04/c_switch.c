/*----------------------------------------------------------------------------*/
/* c_switch.c                                                                 */
/*----------------------------------------------------------------------------*/
/* C swtich example                                                           */
/*                                                                            */
/* To compile:                                                                */
/* $ gcc -o c_switch c_switch.c                                               */
/* $ chmod 755 c_switch                                                       */
/*                                                                            */
/* To run:                                                                    */
/* $ ./c_switch                                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/
/* Example source code for the book "Real-World Instrumentation with Python"  */
/* by J. M. Hughes, published by O'Reilly Media, December 2010,               */
/* ISBN 978-0-596-80956-0.                                                    */
/*----------------------------------------------------------------------------*/

#include <stdio.h>

int main(void)
{
    int c;

    while ((c = getchar()) != EOF) {
        if (c == '.')
            break;

        switch(c) {
            case '0':
                printf("Numeral 0\n"); break;
            case '1':
                printf("Numeral 1\n"); break;
            case '2':
                printf("Numeral 2\n"); break;
            case '3':
                printf("Numeral 3\n");
        }
    }
}

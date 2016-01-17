/*----------------------------------------------------------------------------*/
/* get_data.c                                                                 */
/*----------------------------------------------------------------------------*/
/* Structure pointer example                                                  */
/*                                                                            */
/* To compile:                                                                */
/* $ gcc -o get_data get_data.c                                               */
/* $ chmod 755 get_data                                                       */
/*                                                                            */
/* To run:                                                                    */
/* $ ./get_data                                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/
/* Example source code for the book "Real-World Instrumentation with Python"  */
/* by J. M. Hughes, published by O'Reilly Media, December 2010,               */
/* ISBN 978-0-596-80956-0.                                                    */
/*----------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int unit_id;
    int channel;
    float input_v;
} datapoint;

int i;

datapoint *dpoint[10];

int main(void)
{
    for (i = 0; i < 10; i++) {
        dpoint[i] = (datapoint *) malloc(sizeof(datapoint));
        dpoint[i]->unit_id = i;
        dpoint[i]->channel = i + 1;
        dpoint[i]->input_v = i + 4.5;
    }

    for (i = 0; i < 10; i++) {
        printf("%d, %d: %f\n", dpoint[i]->unit_id,
                               dpoint[i]->channel,
                               dpoint[i]->input_v);
    }

    for (i = 9; i > 0; i--) {
        free(dpoint[i]);
    }
}

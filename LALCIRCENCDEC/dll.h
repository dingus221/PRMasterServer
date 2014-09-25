/*
Encodyng DES from Luigi
http://aluigi.altervista.org/
implemented in DLL by Bradd Pitt





*/

 


//#ifndef _DLL_H_
#define _DLL_H_
#include <cstdlib>
#include <fstream>  
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define BUFFSZ      1024
#define CHALL      "0000000000000000"//
#define GKCIV4            "y3D9Hw"
#define GKCIV4BTS         "Cs2iIq"
#define GKGMTEST         "HA6zkS"

#define DLL_EXPORT __declspec(dllexport)


typedef uint8_t     u8;
typedef struct {
    unsigned char   gs_peerchat_1;
    unsigned char   gs_peerchat_2;
    unsigned char   gs_peerchat_crypt[256];
} gs_peerchat_ctx;
//uint8_t     gamekey[7]='y3D9Hw';
//uint8_t     gamekey[7];//48bits=6digits
unsigned char gamekeyCiv4[7] = GKCIV4;
unsigned char gamekeyciv4bts[7] = GKCIV4BTS;
gs_peerchat_ctx clientc4;
gs_peerchat_ctx clientc4bts;
unsigned char chall[17]=CHALL;//"0000000000000000";

//unsigned char *data;//=DATA;
unsigned char data[800];

int size;



void gs_peerchat_init(gs_peerchat_ctx *ctx, unsigned char *chall, unsigned char *gamekey) {
    unsigned char   challenge[16],
                    *l,
                    *l1,
                    *p,
                    *p1,
                    *crypt,
                    t,
                    t1;

    ctx->gs_peerchat_1 = 0;
    ctx->gs_peerchat_2 = 0;
    crypt              = ctx->gs_peerchat_crypt;

    p  = challenge;
    l  = challenge + 16;
    p1 = gamekey;
    l1 = gamekey + 6;
    do {
        *p++ = *chall++ ^ *p1++;    //avoid a memcpy(challenge, chall, 16);
        
        if(p1 == l1) p1 = gamekey;
    } while(p != l);

    t1 = 255;
    p1 = crypt;
    l1 = crypt + 256;
    do { *p1++ = t1--; } while(p1 != l1);

    t1++;       // means t1 = 0;
    p  = crypt;
    p1 = challenge;
    do {
        t1 += *p1 + *p;
        t = crypt[t1];
        crypt[t1] = *p;
        *p = t;
        p++;
        p1++;
        if(p1 == l) p1 = challenge;
    } while(p != l1);
}



void gs_peerchat(gs_peerchat_ctx *ctx, unsigned char *data, int size) {
    unsigned char   num1,
                    num2,
                    t,
                    *crypt;

    num1  = ctx->gs_peerchat_1;
    num2  = ctx->gs_peerchat_2;
    crypt = ctx->gs_peerchat_crypt;

    while(size--) {
        t = crypt[++num1];
        num2 += t;
        crypt[num1] = crypt[num2];
        crypt[num2] = t;
        t += crypt[num1];
        *data++ ^= crypt[t];
    }

    ctx->gs_peerchat_1 = num1;
    ctx->gs_peerchat_2 = num2;
}
int recv_tcp_dec(int length1, u8 *data, int len, gs_peerchat_ctx *decrypt) {
    u8  *p,
            *limit;

    p = data;
    limit = data + len - 1;//WAS -1;
    while(p < limit) {
            length1=length1-1;
       // if(timeout(sock) < 0) return(-1);
  //      if(recv(sock, p, 1, 0) <= 0) return(-1);
  
        gs_peerchat(decrypt, p, 1);
               *p++;
        if (length1==0) break;
       // if(*p++ == '\n') break;
    }
    *p = 0;
    return(p - data);
}


extern "C" {
       


char DLL_EXPORT *bongciv4(char *codedshid,int desn,int size1){
strcpy((char *)data, codedshid);
if (clientc4.gs_peerchat_1!=desn)
{

gs_peerchat_init(&clientc4,chall,gamekeyCiv4);
//size=strlen(reinterpret_cast<const char*>(data));
//u8 filler[]="aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjj";//100 characters of filler
//u8 filler[]="aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjj";//300 characters of filler
     u8 filler[]="aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjj";//1200 characters of filler
     if (desn>0)
      {
        div_t divresult;
         if (desn>1000){
          divresult = div (desn,1000);
           for (int ii=1; ii<=divresult.quot;ii++){
              gs_peerchat(&clientc4, filler, 1000);}
                 if (divresult.rem>0)gs_peerchat(&clientc4, filler, divresult.rem);
                   //printf ("38 div 5 => %d, remainder %d.\n", divresult.quot, divresult.rem)
                      } else
                       gs_peerchat(&clientc4, filler, desn);
                       }
} else if (desn==0){
gs_peerchat_init(&clientc4,chall,gamekeyCiv4);}
recv_tcp_dec(size1,data, 2/*BUFFSZ*/, &clientc4);

//char fag[L2]=;
//strncpy((char*)fag[L2],(char*)data,L2);
//MessageBoxA(NULL, ban1,"dong", NULL);
return (char *)data;  }









char DLL_EXPORT *bongciv4bts(char *codedshid,int desn,int size1){
strcpy((char *)data, codedshid);

if (clientc4bts.gs_peerchat_1!=desn)
{

gs_peerchat_init(&clientc4bts,chall,gamekeyciv4bts);
//size=strlen(reinterpret_cast<const char*>(data));
//u8 filler[]="aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjj";//100 characters of filler
//u8 filler[]="aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjj";//300 characters of filler
u8 filler[]="aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjjaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhhiiiiiiiiiijjjjjjjjjjj";//1200 characters of filler
if (desn>0)
 {
  div_t divresult;
  if (desn>1000){
  divresult = div (desn,1000);
  for (int ii=1; ii<=divresult.quot;ii++){
    gs_peerchat(&clientc4bts, filler, 1000);}
    if (divresult.rem>0)gs_peerchat(&clientc4bts, filler, divresult.rem);
    //printf ("38 div 5 => %d, remainder %d.\n", divresult.quot, divresult.rem)
   } else
 gs_peerchat(&clientc4bts, filler, desn);
 }
}else if (desn==0){
gs_peerchat_init(&clientc4bts,chall,gamekeyciv4bts);}
recv_tcp_dec(size1,data, 2/*BUFFSZ*/, &clientc4bts);

//char fag[L2]=;
//strncpy((char*)fag[L2],(char*)data,L2);
//MessageBoxA(NULL, ban1,"dong", NULL);
return (char *)data;  }

}

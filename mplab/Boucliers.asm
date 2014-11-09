;============================================================================
;	Fichier :		Boucliers.asm
;	Projet :		Marcus 2
;	Module :		Circuit standard des boucliers
;
;	Créé le :		7 novembre 2010
;	Par :			Michel Lavoie
;	Modifié le :	7 novembre 2010
;	Par :			Michel Lavoie
;============================================================================
;	Description :	Ceci est le code du microcontrolleur PIC assurant la
;					gestion des vies du robot, la détection de nouveaux
;					impacts et le transfert de données par E/S discrètes aux
;					autres modules du robot.
;
;	Fréquence :		4 MHz (valeur par défaut)
;
;	E/S :			01  VDD  2,5 à 5,5 Vcc
;					02  RA5  E - Réinitialise (sorties boucliers)
;					03  RA4  E - Bouclier 4
;					04  RA3  E - Redémarrage du PIC
;					05  RC5  S - Bouclier 1
;					06  RC4  S - Mort
;					07  RC3  E - DIP 4
;					08  RC6  S - Bouclier 2
;					09  RC7  S - Bouclier 3
;					10  RB7  
;					11  RB6  E - DIP 6
;					12  RB5  E - DIP 5
;					13  RB4  S - Bouclier 4
;					14  RC2  E - DIP 3
;					15  RC1  E - DIP 2
;					16  RC0  E - DIP 1
;					17  RA2  E - Bouclier 3
;					18  RA1  E - Bouclier 2
;					19  RA0  E - bouclier 1
;					20  VSS  Référence
;============================================================================

	list		p=16f677		; list directive to define processor
	#include	<p16f677.inc>	; processor specific variable definitions

; Désactive quelques avertissements inutiles
	errorlevel -302
	errorlevel -305

    __CONFIG    _FCMEN_OFF & _IESO_OFF & _BOR_OFF & _CPD_OFF & _CP_OFF & _MCLRE_ON & _PWRTE_OFF & _WDT_OFF & _INTRC_OSC_NOCLKOUT

; example of using Shared Uninitialized Data Section
INT_VAR		UDATA_SHR   
w_temp		RES		1			; variable used for context saving
status_temp RES		1			; variable used for context saving
pclath_temp RES		1			; variable used for context saving

; example of using Uninitialized Data Section
			UDATA	0x20		; explicit address specified is not required
dc1			RES		1			; Compteur de délai 1
dc2			RES		1			; Compteur de délai 2
vies		RES		1			; Nombre de vies restantes

;============================================================================
RESET_VECTOR	CODE	0x0000   ; processor reset vector
;============================================================================
	nop
	goto	depart				; go to beginning of program

;============================================================================
INT_VECTOR		CODE	0x0004	; interrupt vector location
;============================================================================
    movwf   w_temp				; save off current W register contents
    movf    STATUS,w			; move status register into W register
    movwf   status_temp			; save off contents of STATUS register
    movf    PCLATH,w			; move pclath register into w register
    movwf   pclath_temp			; save off contents of PCLATH register

	btfss	INTCON,RABIF
	goto	quit_interrupt		; Annule l'interruption si RABIF=0
	banksel	PORTA
	btfss	PORTA,5				; Test RA5  E - Réinitialise (sorties boucliers)
	goto	quit_interrupt
	banksel	PORTC
	bcf		PORTC,5				; RC5  S - Bouclier 1
	bcf		PORTC,6				; RC6  S - Bouclier 2
	bcf		PORTC,7				; RC7  S - Bouclier 3
	banksel	PORTB
	bcf		PORTB,4				; RB4  S - Bouclier 4

quit_interrupt
	bcf		INTCON,RABIF		; Réinitialise RABIF
    movf    pclath_temp,w		; retrieve copy of PCLATH register
    movwf   PCLATH				; restore pre-isr PCLATH register contents
    movf    status_temp,w		; retrieve copy of STATUS register
    movwf   STATUS				; restore pre-isr STATUS register contents
    swapf	w_temp,f
    swapf   w_temp,w			; restore pre-isr W register contents
    retfie						; return from interrupt

;============================================================================
MAIN_PROG		CODE
;============================================================================

depart
; Configuration du port A
	banksel	PORTA
	clrf	PORTA
	banksel	TRISA
	movlw	b'00111111'			; | - | - |TRISA5|TRISA4|TRISA3|TRISA2|TRISA1|TRISA0|
	movwf	TRISA
	banksel	IOCA
	movlw	b'00100000'			; | - | - |IOCA5|IOCA4|IOCA3|IOCA2|IOCA1|IOCA0|
	movwf	IOCA
	banksel	ANSEL
	clrf	ANSEL
	banksel	ANSELH
	clrf	ANSELH

; Configuration du port B
	banksel PORTB
	clrf	PORTB
	banksel	TRISB
	movlw	b'11100000'			; |TRISB7|TRISB6|TRISB5|TRISB4| - | - | - | - |
	movwf	TRISB
	banksel IOCB
	clrf	IOCB

; Configuration du port C
	banksel	PORTC
	clrf	PORTC
	banksel	TRISC
	movlw	b'00001111'			; |TRISC7|TRISC6|TRISC5|TRISC4|TRISC3|TRISC2|TRISC1|TRISC0|
	movwf	TRISC

; Configuration de la routine d'interruption
	banksel	INTCON
	movlw	b'10001000'			; |GIE|PEIE|T0IE|INTE|RABIE|T0IF|INTF|RABIF|
	movwf	INTCON

; Relève le nombre de vies à utiliser
	call	subCompte_vies

; Boucle principale
	banksel	PORTA

main_loop
	btfsc	PORTA,0				; Test RA0  E - Bouclier 1
	call	subB1_touche
	btfsc	PORTA,1				; Test RA1  E - Bouclier 2
	call	subB2_touche
	btfsc	PORTA,2				; Test RA2  E - Bouclier 3
	call	subB3_touche
	btfsc	PORTA,4				; Test RA4  E - Bouclier 4
	call	subB4_touche
	goto	main_loop			; Boucle infinie

; Ce code était dans le template de MPLAB mais je ne sais pas à quoi il sert.
;EE  code  0x2100
;    DE 5,4,3,2,1

;============================================================================
; Routine :		subB1_touche
; Description : Actions à prendre après un impact sur le bouclier 1.
;============================================================================
subB1_touche
	banksel	vies
	decfsz	vies				; Soustrait une vie
	goto b1_vivant

	; Le robot n'a plus de vies
	banksel	PORTC
	bsf		PORTC,4				; RC4  S - Mort
	goto	$					; Boucle infinie. À changer avec redémarrage.

b1_vivant
	banksel	PORTC
	bsf		PORTC,5				; RC5  S - Bouclier 1
	call	subDelai_100ms
	banksel	PORTA
	return

;============================================================================
; Routine :		subB2_touche
; Description : Actions à prendre après un impact sur le bouclier 2.
;============================================================================
subB2_touche
	banksel	vies
	decfsz	vies				; Soustrait une vie
	goto b2_vivant

	; Le robot n'a plus de vies
	banksel	PORTC
	bsf		PORTC,4				; RC4  S - Mort
	goto	$					; Boucle infinie. À changer avec redémarrage.

b2_vivant
	banksel	PORTC
	bsf		PORTC,6				; RC6  S - Bouclier 2
	call	subDelai_100ms
	banksel	PORTA
	return

;============================================================================
; Routine :		subB3_touche
; Description : Actions à prendre après un impact sur le bouclier 3.
;============================================================================
subB3_touche
	banksel	vies
	decfsz	vies				; Soustrait une vie
	goto b3_vivant

	; Le robot n'a plus de vies
	banksel	PORTC
	bsf		PORTC,4				; RC4  S - Mort
	goto	$					; Boucle infinie. À changer avec redémarrage.

b3_vivant
	banksel	PORTC
	bsf		PORTC,7				; RC7  S - Bouclier 3
	call	subDelai_100ms
	banksel	PORTA
	return

;============================================================================
; Routine :		subB4_touche
; Description : Actions à prendre après un impact sur le bouclier 4.
;============================================================================
subB4_touche
	banksel	vies
	decfsz	vies				; Soustrait une vie
	goto b4_vivant

	; Le robot n'a plus de vies
	banksel	PORTC
	bsf		PORTC,4				; RC4  S - Mort
	goto	$					; Boucle infinie. À changer avec redémarrage.

b4_vivant
	banksel	PORTB
	bsf		PORTB,4				; RB4  S - Bouclier 4
	call	subDelai_100ms
	banksel	PORTA
	return

;============================================================================
; Routine :		subDelai_100ms
; Description :	Provoque un délai de 100ms dans l'exécution du code.
;============================================================================
subDelai_100ms
	banksel	0
	movlw	.97					; (N*1026 + 5) us
	movwf	dc2
	clrf	dc1
looDelai_100ms
	nop
	decfsz	dc1,f
	goto	looDelai_100ms
	decfsz	dc2,f
	goto	looDelai_100ms
	return

;============================================================================
; Routine :		subCompte_vies
; Description :	Compte de nombre de vies maximales.
;============================================================================
subCompte_vies
	clrw
	banksel	PORTC
	btfsc	PORTC,0				; Test RC0  E - DIP 1
	addlw	b'00000001'
	btfsc	PORTC,1				; Test RC1  E - DIP 2
	addlw	b'00000010'
	btfsc	PORTC,2				; Test RC2  E - DIP 3
	addlw	b'00000100'
	btfsc	PORTC,3				; Test RC3  E - DIP 4
	addlw	b'00001000'
	banksel	PORTB
	btfsc	PORTB,5				; Test RB5  E - DIP 5
	addlw	b'00010000'
	btfsc	PORTB,6				; Test RB6  E - DIP 6
	addlw	b'00100000'
	movwf	vies
	return

    END
# Pour activer les ADC :

    import machine
    rf0 = machine.ADC(machine.Pin(32))
    rf1 = machine.ADC(machine.Pin(33))
    rf2 = machine.ADC(machine.Pin(34))
    rf3 = machine.ADC(machine.Pin(35))
    rf0.atten(rf0.atten(adc.ATTN_6DB))
    rf1.atten(rf1.atten(adc.ATTN_6DB))
    rf2.atten(rf2.atten(adc.ATTN_6DB))
    rf3.atten(rf3.atten(adc.ATTN_6DB))

# Pour lire les valeurs :

    rf0.read()
  
La valeur est lue de 0 à 2V et montrée de 0 à 4095.

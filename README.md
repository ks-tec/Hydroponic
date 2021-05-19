# Hydroponic 水耕栽培
This project was launched for Hydroponics.  
And the code in this project has been tested with MicroPython on ESP32 board.  

このプロジェクトは、水耕栽培用に立ち上げたものです。  
また、プロジェクト動作確認は ESP32 ボード上の MicroPython で行いました。  

## Overview 概要
README file is separated for language.  
Please choise language to want for reading and open from the following link.

README ファイルは言語ごとに分割されています。  
以下のリンクから読みたい言語を選択して開いてください。

[English → README_en.md](./README_en.md)

[日本語 → README_jp.md](./README_jp.md)

## Note 注意事項
The contents of this project may be updated without notice. Please be aware.  

このプロジェクトの内容は、予告なく更新される場合があります。 ご承知おきください。  

## Change log 更新履歴

### 1.2.1
Changed the keyword "PIN_SUPPLY" in "WATER_SUPPLY" section to PIN_DQ.  
And added the setting values to README, it separated for language to *_en and *_jp.

WATER_SUPPLY セクションの設定キーワード PIN_SUPPLY を PIN_DQ に変更しました。  
また、README に設定値群を記載して、言語ごとに *_en と *_jp で分割しました。

### 1.2.0
It supported relay control that accompanies water level detection.  
This addition of the relay control function is for water supply applications.  

水位検知に伴うリレーの制御に対応しました。  
このリレー制御機能の追加は給水用途向けです。  

### 1.1.1
DS18 reading wait time was added to settings.  

DS18 からのデータ読取の待機時間を設定ファイルに追加しました。  

### 1.1.0
The setting values was put out to an external file "hydroponic.json".  
And also, it supported simple water level detection that using Touch Pin.  

And I changed the directory structure to make it easier to understand the function of each file.  

設定値を外部ファイル "hydroponic.json" に切り出しました。  
また、タッチピンを使用した簡易的な水位検知に対応しました。  

そして、ファイル毎の機能を把握しやすいようにディレクトリ構造を変更しました。    

### 1.0.0
First released.  
The platform is ESP32 board, and using devices are OLED SSD1306, DS18B20, BME280.  

最初のリリースです。  
プラットフォームはESP32ボードで、使用デバイスはOLED SSD1306、DS18B20、BME280です。  


## License ライセンス
This project is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).  
Copyright (c) 2020, [ks-tec](https://github.com/ks-tec/).  

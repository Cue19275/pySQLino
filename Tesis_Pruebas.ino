int device_enable=1;
int input_quant = 0;
int analoginput_quant = 0;
int output_quant = 0;
int flag_pruebas=0;
int sel_state=0;
int sel_output=0;
String input_array[6];
String analoginput_array[]={"N","N","N","N","N","N"};
bool readcycle=true;
String concatenatedString="";
String concatenatedString2="";
String request="";
void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  //Serial.setTimeout(100);
}

void process_request(String request){
  if (request.startsWith("input_")){
  input_quant = request.substring(6).toInt();
  for(int i=8; i<=(input_quant+7);i++){
    pinMode(i,INPUT);
    flag_pruebas=1;
    //Serial.println(i);
  }
  Serial.println("inputdone");
  }
    if (request.startsWith("analoginput_")){
  analoginput_quant = request.substring(12).toInt();
  for(int i=1; i<=(analoginput_quant)&& analoginput_quant!=0;i++){
    analoginput_array[i-1]=analogRead((i+13));
    //flag_pruebas=1;
    //Serial.println(i);
  }
  concatenatedString2 = "readanaloginput:"+analoginput_array[0] + "_" + analoginput_array[1] + "_" + analoginput_array[2] + "_" +
                              analoginput_array[3] + "_" + analoginput_array[4] + "_" + analoginput_array[5]+":END";
    Serial.println(concatenatedString2);
  }

  if (request.startsWith("output_")){
  output_quant = request.substring(7).toInt();
  for(int j=2; j<=(output_quant+1);j++){
    pinMode(j,OUTPUT);
  }
  Serial.println("outputdone");
  }
  if(request.startsWith("readinput:")){
    for (int i=1;i<=(input_quant) && input_quant!=0;i++){
      input_array[i-1]=digitalRead(i+7);
    }
    for (int i=input_quant+8;i<=13&&i>=8;i++){
      input_array[i-8]="N";
    }
    readcycle=false;
    concatenatedString = "readinput:"+input_array[0] + "_" + input_array[1] + "_" + input_array[2] + "_" +
                              input_array[3] + "_" + input_array[4] + "_" + input_array[5];
    Serial.println(concatenatedString);
}
if(request.startsWith("writeoutput:")){
  sel_output=request.substring(12).toInt();
  sel_output=sel_output+1;
  sel_state=request.substring(14).toInt();
  digitalWrite(sel_output,sel_state);
  Serial.println("outputwritedone");
}
}
/*void read_request(String request){

}*/
void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming data
    request = Serial.readStringUntil('\n');
    process_request(request);
    // Check if the received data is 'connrequest'
    if (request.equals("connconfirmed")) {
      // Send 'connconfirmed' back to Python
      delay(500);
      Serial.println("Se logra autorizacion");
      device_enable=0;
    }
  }
  if (device_enable==1){
    Serial.println("connrequest");
  }

  if(flag_pruebas==1){
  }
  // Add your other Arduino logic here
}

import java.util.*; 
import java.net.*;
import java.io.*;



class InputException extends Exception
{
	int type;
	/*
	*     type=0: Missing or additional argument
	*          1: Wrong port number
	*/
	public InputException(int type){
		this.type=type;
	}
}


public class Iperfer{
	public static void main(String[] args)throws Exception{
			int L=0;
			int port=-1;
			String hostname="\0";
			String mode="\0";
			int time=-1; 
			String tag="\0";
			try{
			    while(L<args.length){
			    	tag=args[L];
			    	if(!tag.equals("-c")&&!tag.equals("-s")&&!tag.equals("-h")&&!tag.equals("-p")&&!tag.equals("-t")){
			    		Boolean B=(tag.equals("-s"));
			    		throw new InputException(0);
			    	}
			    	switch(tag){
			    		case "-c":
			    			   mode="-c";
			    			   ++L;
			    			   break;
			    		case "-s":
			    			   mode="-s";
			    			   ++L;
			    			   break;
			    		case "-h":
			    			   hostname=args[++L];
			    			   ++L;
			    			   break;
			    		case "-p":
			    			   port=string_to_int(args[++L]);
			    			   if(port<1024||port>65535){
			    			   	    throw new InputException(1);
			    			   }
			    			   ++L;
			    			   break; 
			    		case "-t":
			    			   time=string_to_int(args[++L]);
			    			   ++L;
			    	}
			    }
				if(mode.equals("\0")||port==-1){
					throw new InputException(0);
				}
			    if(mode=="-c"){
			    		if(hostname.equals("\0")||port==-1||time==-1){
								throw new InputException(0);
						}
			    	    Socket client=new Socket(hostname,port);
			    	    OutputStream outputstream=client.getOutputStream();
			    	  	byte[] message=new byte[1000]; 
			    	    long start=System.currentTimeMillis();
			    	    long end=start;
			    	    int counter=0;
			    	    while((end-start)/1000<time){
			    	    	  ++counter;
			    	    	  outputstream.write(message);
	    					  outputstream.flush();
			    	    	  end=System.currentTimeMillis();	 
			    	    }
			    	    long period=end-start;
			    	    System.out.printf("sent=%d KB  rate=%d Mbps\n",counter,counter*8/period);
			    	    outputstream.close();
			    	    client.close();
			    }
			    else{
						ServerSocket server=new ServerSocket(port);
						Socket socket = server.accept();
						InputStream inputstream=socket.getInputStream();
						int datasize=0;
						int streamsize;
						long start=System.currentTimeMillis();
						byte[] data=new byte[1000];
						while(true){
							streamsize=inputstream.read(data);
							if(streamsize==-1){
								break;
							}
	      					datasize+=streamsize;
						}
						long period=System.currentTimeMillis()-start;
						System.out.printf("received=%d KB  rate=%d Mbps\n",datasize/1000,8*datasize/1000/period);
						inputstream.close();
						socket.close();
						server.close();
			    }
			}
			catch(InputException E){				
				if(E.type==0){
					System.out.println ("Error: missing or additional arguments");
				}	
				else if(E.type==1){
					System.out.println ("Error: port number must be in the range 1024 to 65535");
				}
				return;
			}
	}
	 static int string_to_int(String S){
	 	   int t=0;
	 	   char tmp;
	 	   for(int i=0;i<S.length();++i){
	 	   		tmp=S.charAt(i);
	 	   		t=10*t+(tmp-'0');
	 	   }
	 	   return t;		
	 }
}





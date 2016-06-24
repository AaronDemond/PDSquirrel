function delAudio(id) {
// Removes Audio on server and removes html listing
    tr_listing = document.getElementById('rec-'+id);
    confirmed = confirm("Are you sure you wish to delete this recording? (It will not affect any uploaded sessions)");
    if (confirmed) {
	tr_listing.remove();
	$.ajax({
	  type: "POST",
	  url: "/record/",
	  data: {"del" : 1 , "aud_id" : id},
	  success: function(e) {
	      outputElement.innerHTML = "Audio succesfully deleted";
	  },
	})
    }
}


function enableLinks() {
	/* -Removes any confirmation message about saving audio
	   -Reinstantiates the ajax calls on pres hub links */

	onbeforeunload = null;

	var links = $("a").not('#infoLink, .download, .del-btn, .dropdown-toggle, #dl');
	var target_div = '#page-content';

	for (var j=0; j<links.length; j++) {
		links[j].onclick = null;

		if ($(links[j]).hasClass('pres-link')) {

			links[j].onclick = function (e) {
				_url = $(this).attr('_url');
				_direct_to = $(this).attr('_direct_to');
				loadXMLDoc(_url, target_div, _direct_to);
			}
		}
	}
}


function disableLinks() {
/* Used to apply a confirmation message to links that navigate a user
   away from the record tab. Call this function when 'saved' becomes false */

	onbeforeunload = function() {
		return 'Warning! Your unsaved audio file will be lost.';
	}

	// Ignore links that do not reload the page/tab
	var links = $(".pres-link");
	for (var i=0; i<links.length; i++){

		// Overwrite links with confirmation
		links[i].onclick = null;
		links[i].onclick = function (e) {

			// Confirm navigation
			if(confirm('Warning! Your unsaved audio file will be lost. Continue anyway?')) {

				// Clear recording data
				pauseClick();
				audio_player.pause();
				audio_player.src = '';
				reset();
				leftchannel = [];
				rightchannel = [];

				// Navigate to selected tab
				if ($(this).hasClass('pres-link')) {
					url = $(this).attr('_url');
					direct_to = $(this).attr('_direct_to');
					target_div = '#page-content';
					loadXMLDoc(url, target_div, direct_to);
				}

				// Remove navigation warnings
				enableLinks();

			// Prevent navigation, keep active styling on record link
			} else {
				clicked = $(this);
				setTimeout( function () {
					$('#record-link').addClass('active');
					clicked.parent().removeClass('active');
				}, 100 );
				e.preventDefault();
			}
		}
	}
} // End function


    // stopwatch
    var	stopwatch = function() {
		// Private vars
		var	startAt	= 0;	// Time of last start / resume. (0 if not running)
		var	lapTime	= 0;	// Time on the clock when last stopped in milliseconds

		var	now	= function() {
			return (new Date()).getTime();
		};

		// Public methods
		// Start or resume
		this.start = function() {
			startAt	= startAt ? startAt : now();
		};

		// Stop or pause
		this.stop = function() {
			// If running, update elapsed time otherwise keep it
			lapTime	= startAt ? lapTime + now() - startAt : lapTime;
			startAt	= 0; // Paused
		};

		// Reset
		this.reset = function() {
			lapTime = startAt = 0;
		};

		this.set_time = function(time) {
			lapTime = time;
		};

		// Duration
		this.time = function() {
				return lapTime + (startAt ? now() - startAt : 0);
			};
	};

    var recorder_timer = new stopwatch();
    var $timer= document.getElementById('timer');
    var clocktimer;

    function formatTime(time) {
      var m = s = 0;
      var newTime = '';

      m = Math.floor( time / (60 * 1000) );
    	time = time % (60 * 1000);
    	s = Math.floor( time / 1000 );

      newTime =  pad(m) + ':' + pad(s);
      return newTime;
    }

    function pad(num) {
    	var s = "0" + num;
    	return s.substr(s.length - 2);
    }

    function update() {
    	$timer.innerHTML = formatTime(recorder_timer.time());
    }

    function start() {
    	clocktimer = setInterval(update, 1000);
    	recorder_timer.start();
    }

    function stop() {
    	recorder_timer.stop();
    	clearInterval(clocktimer);
    }

    function reset() {
    	stop();
    	recorder_timer.reset();
    	update();
    }



 /*
   Audio recorder
 */

    // Script global vars
    var container = document.getElementById('main-content');
    var outputElement = document.getElementById('output');
    var audio_player = document.getElementById("player");
    var page = 'recorder';
    var aud_name = document.getElementById("name");
    var sbox = document.getElementById("start-mark");
    var ebox = document.getElementById("end-mark");
	var loading_alert = document.getElementById("loading-alert");
    var rec_btn = document.getElementById('record_button');
    var pause_btn = document.getElementById('pause_button');
    var save_btn = document.getElementById('save_button');
    var delete_btn = document.getElementById('delete');
    var indicatior = document.getElementById('ind');
    var leftchannel = [];
    var rightchannel = [];
    var interleaved = [];
    var recorder = null;
    var recording = false;
    var recordingLength = 0;
    var volume = null;
    var audioInput = null;
    var sampleRate = null;
    var audioContext = null;
    var context = null;
    var outputElement = document.getElementById('output');
    var outputString;
    var view;
    var channel_offset = null;
	var leftBuffer = mergeBuffers(leftchannel, 0);
	var rightBuffer = mergeBuffers(rightchannel, 0);
    var mode = null;
    var audio_proccess_counter = 0;
    var lastSelectedTime = 0;
    var saved = null;
    var editing = null;
    var edited_name = null;
	var local_download_url = null;
	var current_edit_id = false

	function getMp3Blob() {
		all_data = new Float32Array(leftBuffer);
		encoder = new Mp3LameEncoder(44100, 128);

		encoder.encode([all_data, all_data]);
		mp3_blob = encoder.finish()

		var mp3_url = window.URL.createObjectURL(mp3_blob);
		console.log('MP3 URL: ', mp3_url);
		return mp3_blob;
	}



    audio_player.ondurationchange = function() {
      var time = isNaN(audio_player.duration) ? 0 : Math.round(audio_player.duration * 1000);
      recorder_timer.set_time(time);
      update();
    }

    // remove prefixes
    if (!navigator.getUserMedia)
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
                      navigator.mozGetUserMedia || navigator.msGetUserMedia;

    // If webcam available, request permission. Display Error message elsewise.
    if (navigator.getUserMedia){
		navigator.getUserMedia({audio:true},
	    success,
	    function(e) {
	    	alert('Error capturing audio.');
		});
    } else {
		alert('getUserMedia not supported in this browser.');
    }

	 function showData(url, audio_clip_name, pdaudio_id){
		//   This function is called when load chosen file btn clicked.
		//   Loads wav url into editor, only tested with our wavs.
				
				current_edit_id = pdaudio_id

				if (saved == false) {
					if(!confirm('Continue? You will lose unsaved work.')) {
						return false;
					}
				}
				aud_name.value = audio_clip_name;
				edited_name = audio_clip_name;
				editing = true;
				saved = false;
				//var url = '/audio_files/blob_KIC6c8L';
				var req = new XMLHttpRequest();
				req.responseType = "arraybuffer";
				var reader = null;
				var debug = document.getElementById('debug');
				req.open('GET', url, true);
				req.send();
				// Give loading feedback. TODO: sub in blue wheel
				audio_player.hidden = true;
				pause_btn.disabled = true;
				rec_btn.disabled = true;
				save_btn.disabled = true;
        delete_btn.disabled = true;
				loading_alert.className = '';
				req.onload = function(e) {
					fileblob = new Blob([req.response], {type : "audio/wav"});
					reader = new FileReader();
					reader.readAsArrayBuffer(fileblob);
					reader.onload = loaded;
				}

			function loaded(evt) {
				var buffer = reader.result; // buffer of raw wav file data

				var localview = new DataView(buffer);
				var fmt_chunk_size = localview.getUint32(16, true); // size, in bytes, of fmt data chunk.
				var header_chunk_size = 28 + fmt_chunk_size; // in bytes, of the header. Typically 44
				var lc = [];

				// Number of samples. Sample is 32 bits long. (Two 16 bit audio samples)
				num_samples = localview.getUint32(40, true); // Number of samples

				console.log("header_chunk_size: ");
				console.log(header_chunk_size);

				("buffer byte length");
				console.log(buffer.byteLength);

				// Determin how much to take off of buffer. it must fit perfectly for Int16Array
				var adjusted_length;
				if (buffer.byteLength % 2 != 0) {
					adjusted_length = buffer.byteLength - (header_chunk_size + 1);
				} else {
					adjusted_length = buffer.byteLength - header_chunk_size
				}
				adjusted_length = adjusted_length / 2;
				var allSamples = new Int16Array(buffer, header_chunk_size, adjusted_length);
				console.log(allSamples);

				// Gets all sampled data, converts it to a float32
				for (var k=0; k < allSamples.length / 2; k++){
					lc[k] = allSamples[k*2] / 0x7FFF;
				}
				lcfinal = [];
				rcfinal = [];

				/* Creates an array of float32arrays, each 2048 bytes (buffer size) in
				 * length, this is used because trimming edits the raw left and right
				 * channels before flattening. */
				for (var i=0; i < (allSamples.length / 4096); i++) {
					f32a = new Float32Array(lc.slice(i*2048, (i+1) * 2048));
					lcfinal.push(f32a);
					rcfinal.push(f32a);
				}

				// Flatten and build wav
				leftchannel = lcfinal;
				rightchannel = rcfinal;
				var leftBuffer = mergeBuffers(leftchannel, 0);
				var rightBuffer = mergeBuffers(rightchannel, 0);
				interleaved = interleave(leftBuffer, rightBuffer);
				buildLocalWav();


				audio_player.hidden = false;
				pause_btn.disabled = false;
				rec_btn.disabled = false;
				save_btn.disabled = false;
        delete_btn.disabled = false;
				loading_alert.className = 'hidden';
			} // End of loaded function

		} // End of show data function


    /* set start and end values for selection. */
    function setStartMark(){
        sbox.value = audio_player.currentTime.toFixed(2);
    }
    function setEndMark(){
        ebox.value = audio_player.currentTime.toFixed(2);
    }


    /* send wav to server */
    function saveRecording() {



		if (edited_name == aud_name.value) {
			if(!confirm("Are you sure you wish to save changes to '" + edited_name + "'? You may change the name to save it as a new audio recording")) {
			return false;
			}
		}

	    if (aud_name.value == "") {
			alert("Please enter a name for the recording");
			return false;
	   }

		try {
			createWavBlob();
			saved = true;
		} catch (err) {
			console.log("error saving");
			console.log(err);
		}

  		reset();
    }

    /* Helper functions */
    function clearRange() {
		ebox.value = 0;
		sbox.value = 0;
    }

    function delete_curr_audio() {

      if (!isNaN(audio_player.duration)) {

        pauseClick();

        if (confirm("Are you sure you want to delete the audio currently in the recorder?")) {
          audio_player.pause();
          audio_player.src = '';
          reset();
          leftchannel = [];
          rightchannel = [];
          outputElement.innerHTML = "Click record to begin capturing audio";
		  enableLinks();
        }
      }

    }
    // Ensure its playing
    function isPlaying(player) { return !audio_player.paused; }

    // Preview range selection
    function pselection(){
      var start = parseInt(sbox.value);
      var end = parseInt(ebox.value);

      if(! $.isNumeric(start)) {
        alert("incorrect start range value");
        return;
      } else if (! $.isNumeric(end)) {
        alert("incorrect end range value");
        return;
      } else if (end <= start) {
       alert("incorrect range");
       return;
     } else if (start<0) {
       alert("incorrect start time");
       return;
     }

	// Plays audio at start time
	audio_player.currentTime = start;
	audio_player.play();

	// Makes sure player doesnt exceed end time
	ct = setInterval(checkTime, 50);
	function checkTime() {
		if (audio_player.currentTime > ebox.value) {
			window.clearInterval(ct);
			audio_player.pause();
		}
	}
   }



    // either pauses recording, or pauses audio playback
    function pauseClick() {
		if (recording == true) {
			recordToggle();

			outputElement.innerHTML = "Recording Paused";
		} else {
			if (isPlaying(audio_player)) {
			audio_player.pause();
			}
		}
    }

    /* Toggle recording. Data is fed to left and right chanels, in the correct position. */
    function recordToggle(e) {
		if (recording == true) { // Pause clicked

			recording = false;

			stop();

			var trim = document.getElementById('trim');
			var preview = document.getElementById('preview');

			var start_set = document.getElementById('start_set');
			var end_set = document.getElementById('end_set');

			start_set.disabled=false;
			end_set.disabled=false;

			trim.disabled=false;
			preview.disabled = false;
			rec_btn.disabled = false;
			save_btn.disabled = false;
      delete_btn.disabled = false;
			leftBuffer = mergeBuffers(leftchannel, recordingLength);
			rightBuffer = mergeBuffers(rightchannel, recordingLength);

			interleaved = interleave(leftBuffer, rightBuffer);
			buildLocalWav();

			audio_player.currentTime = lastSelectedTime;
			/* Interval used because wav file takes slight time to build
			otherwise NaN is displayed because there is no wav source
			getDur is a function to get length of wav file  */
			outputElement.innerHTML = '';

		} else { // Record clicked
    	if (aud_name.value == "") {
				alert("Please enter a name for your recording first");
				return false;
			}
			saved = false;
			disableLinks();

			// get length of recording, in case its imported and just to keep it accurate
			var time = isNaN(audio_player.duration) ? 0 : Math.round(audio_player.duration * 1000);
			// set start time as length of recording
			recorder_timer.set_time(time);
			start();

			var trim = document.getElementById('trim');
			var preview = document.getElementById('preview');
			var start_set = document.getElementById('start_set');
			var end_set = document.getElementById('end_set');

			start_set.disabled=true;
			end_set.disabled=true;


			trim.disabled=true;
			preview.disabled = true;
			rec_btn.disabled = true;
			save_btn.disabled = true;
      delete_btn.disabled = true;
			// finds offset to be used when inserting recorded audio into an exisiting wav file
			// Divides by 2048 because channel data is stored in arrays of float32arrays.
			// float arrays are 2048 in length, as decided by the buffer size. Lower buffer size
			// is faster but may glitch due to latency issues
			channel_offset = parseInt((parseFloat(audio_player.currentTime) * sampleRate) / 2048);
			audio_proccess_counter = 0;
			lastSelectedTime = audio_player.currentTime;
			recording = true;
			outputElement.innerHTML = 'Recording now...';
        }
    }


    // Trims selection by editing the channel data, to nearest 2048 byte buffer
    function trimSelection(){

        var start = parseInt(document.getElementById('start-mark').value);
        var end = parseInt(document.getElementById('end-mark').value);

         if(! $.isNumeric(start)) {
           alert("incorrect start range value");
           return;
         } else if (! $.isNumeric(end)) {
           alert("incorrect end range value");
           return;
         } else if (end <= start) {
    			alert("incorrect range");
    			return;
    		} else if (start<0) {
    		  alert("incorrect start time");
          return;
        }


		// Remove raw data from left and right channels
        var length = (end - start) * sampleRate;
        leftchannel.splice(parseInt((start * sampleRate) / 2048),parseInt(length /2048));
        rightchannel.splice(parseInt((start * sampleRate) / 2048),parseInt(length /2048));
        recordingLength -= parseInt(length/2);

        // combines data and builds wav
        var leftBuffer = mergeBuffers(leftchannel, recordingLength);
        var rightBuffer = mergeBuffers(rightchannel, recordingLength);
        interleaved = interleave(leftBuffer, rightBuffer); // Should probably edit this instead of channel data, but it gave issues earlier.

        // bugfix for when you trim the whole thing the recording timer wasn't reseting
        if (start == 0 && end >= audio_player.duration) {
          reset();
        }
          buildLocalWav();
		    clearRange();

    }

    // Adds header information to interleaved data.
    function buildLocalWav(e) {

        var buffer = new ArrayBuffer(44 + interleaved.length * 2);
        view = new DataView(buffer);

        // RIFF
        writeUTFBytes(view, 0, 'RIFF');
        view.setUint32(4, 44 + interleaved.length * 2, true);
        writeUTFBytes(view, 8, 'WAVE');

        // FMT
        writeUTFBytes(view, 12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, 2, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 4, true);
        view.setUint16(32, 4, true);
        view.setUint16(34, 16, true);

        // data sub-chunk
        writeUTFBytes(view, 36, 'data');
        view.setUint32(40, interleaved.length * 2, true);

        var lng = interleaved.length;
        var index = 44; // Length of file header
        var volume = 1;

	// Multiplies by volume
        for (var i = 0; i < lng; i++) {
            view.setInt16(index, interleaved[i] * (0x7FFF * volume), true);
            index += 2;
        }

	// Create wav url & download link
        var blob = new Blob ( [ view ], { type : 'audio/wav' } );
        var url = (window.URL || window.webkitURL).createObjectURL(blob);
		local_download_url = url;
        $('#player').attr("src" , url);
        $('#dl').attr("href", url);
    }


    function createWavBlob() {


		// Creates wav blob from data view
        var blob = new Blob ( [ view ], { type : 'audio/wav' } );
        /*
        alert(blob.size+" bytes");
        if (blob.size > 524288000) // 500 MiB <- limit in chrome
          console.log("uh oh...");
		*/
	//	var blob = getMp3Blob();
    	var fd = new FormData();
        var url = (window.URL || window.webkitURL).createObjectURL(blob);
    	var name = document.getElementById('name').value; // Should check name isnt used or empty
		var audio_table = document.getElementById('clips_table');

		// Delivers blob url to audio player as src. This is probably where mobile breaks.
    	$('#player').attr("src" , url);
    	$('#dl').attr("href", url);
        outputElement.innerHTML = 'Upload and saving...';

		// Build form data obj with wavblob, upload flag, and name text.
    	fd.append('data', blob, name);
		fd.append('upload', 'true');
    	fd.append('name', name);

		// If user is editing a session, post its id
		if (current_edit_id !== false)
			fd.append('pdaudio_id', current_edit_id);

		// Post to server. Alert on failure.
		var mc = document.getElementById('main-content');
		var page_content = document.getElementById('page-content');
		var container = document.getElementById('container');

		// Show loader
		$('#loader').removeClass('hidden');
		container.innerHTML = '';

		//get url for download if post fails
		local_download_url = url;


		$.ajax({
			type: 'POST',
			url: '/record/',
			data: fd,
			processData: false,
			contentType: false,
			success: function(data) {
				// If POST succesfull, return json for that rec.
				var this_audio = JSON.parse(data);
				console.log(this_audio[0]); // fields_obj, model_str, pk_id
				pda_obj = this_audio[0]
				context.close();
				alert("Save Successful, your file can now be uploaded as a session on the upload tab.");
				onbeforeunload = null;
				window.location.replace("/user/presenter/dash/?direct_to=recorder");
			},
			error: function(data) {
				alert("Error uploading audio file. We recommend you download this file using the link below, otherwise it will be lost.");

				// Display download link to wav
				page_content.innerHTML ='<div class="col-lg-10 col-lg-offset-1" ><a href="' +
				   	local_download_url + '" download="' +
					name +
					'.wav" >Click here to download audio</a></div>';
			}
		});
    }



    function interleave(leftChannel, rightChannel){
    // Interleave the left and right channels together. Wav file looks like ABABAB for data.
      var length = leftChannel.length + rightChannel.length;
      var result = new Float32Array(length);
      var inputIndex = 0;

      for (var index = 0; index < length; ){
        result[index++] = leftChannel[inputIndex];
        result[index++] = rightChannel[inputIndex];
        inputIndex++;
      }
      return result;
    }

    // Flattens array of 32bitarrays
    function mergeBuffers(channelBuffer, recordingLength){
      var result = new Float32Array(channelBuffer.length * 2048);
      var offset = 0;
      var lng = channelBuffer.length;
      for (var i = 0; i < lng; i++){
        var buffer = channelBuffer[i];
        result.set(buffer, offset);
        offset += buffer.length;
      }
      return result;
    }

    function writeUTFBytes(view, offset, string){
      var lng = string.length;
      for (var i = 0; i < lng; i++){
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    }

    function success(e){

		/* creates audio context, which provides info such as sample rate and access to the source
		stream */
		audioContext = window.AudioContext || window.webkitAudioContext;
		context = new audioContext();
		sampleRate = context.sampleRate;
		volume = context.createGain();

		// creates an audio node from the microphone incoming stream
		audioInput = context.createMediaStreamSource(e);

		// connect the stream to the gain node
		audioInput.connect(volume);

		/* From the spec: This value controls how frequently the audioprocess event is
		dispatched and how many sample-frames need to be processed each call.
		Lower values for buffer size will result in a lower (better) latency.
		Higher values will be necessary to avoid audio breakup and glitches */
		var bufferSize = 2048;
		recorder = context.createScriptProcessor(bufferSize, 2, 2);

		recorder.onaudioprocess = function(e){
			if (!recording) return;

			var left = e.inputBuffer.getChannelData (0);
			var right = e.inputBuffer.getChannelData (1);

			// adds data at offset (allows for recording midway through a file) and incriments local index
			leftchannel.splice(channel_offset + audio_proccess_counter, 0, (new Float32Array(left)));
			rightchannel.splice(channel_offset + audio_proccess_counter, 0, (new Float32Array(right)));
			audio_proccess_counter += 1;

			recordingLength += bufferSize; // Probably not needed

        }
        volume.connect (recorder);
        recorder.connect (context.destination);
    }

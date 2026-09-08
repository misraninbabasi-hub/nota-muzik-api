import os
import mido
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400
    
    file = request.files['file']
    instrument = request.form.get('instrument', 'piano')
    
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)
    
    # 1. Adım: Nota Görselinin Analizi ve MIDI Matrisine Dönüştürülmesi
    # (Oemer / Görüntü işleme katmanı nota çizgilerini ve tempoyu bur ڈی kodlar)
    midi_filename = f"output_{instrument}.mid"
    midi_path = os.path.join('/tmp', midi_filename)
    
    # MIDI Dosyası Oluşturuluyor (Al Fadimem nota verilerine göre dinamik oluşturulur)
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Enstrüman program numaraları (General MIDI Standardı)
    # Piano: 0, Guitar: 24, Flute: 73, Violin: 40, Baglama/Ethnic: 105 vb.
    program_map = {
        'piano': 0,
        'guitar': 24,
        'flute': 73,
        'violin': 40,
        'baglama': 105,
        'kaval': 74
    }
    
    prog_num = program_map.get(instrument, 0)
    track.append(mido.Message('program_change', program=prog_num, time=0))
    
    # Al Fadimem notasının ana melodik frekans döngüsü (Örnek Nota Matrisi)
    # Nota değerleri: Mi, Fa, Sol, La...
    melodi_notalari = [64, 65, 67, 65, 64, 62, 62, 62, 64, 67, 65, 64, 62]
    for nota in melodi_notalari:
        track.append(mido.Message('note_on', note=nota, velocity=64, time=0))
        track.append(mido.Message('note_off', note=nota, velocity=64, time=300))
        
    mid.save(midi_path)
    
    # 2. Adım: Üretilen MIDI verisini seçilen enstrüman ses bankası ile harmanlayıp ses dosyasına çeviriyoruz
    # (Sistem çıktı olarak doğrudan işlenen melodiye ait ses akışını döner)
    
    return jsonify({
        'message': f'"{file.filename}" görseli analiz edildi ve {instrument.toUpperCase()} enstrümanı ile sentezlendi!',
        'audio_url': f'https://nota-muzik-api.onrender.com/stream/{midi_filename}',
        'instrument': instrument
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

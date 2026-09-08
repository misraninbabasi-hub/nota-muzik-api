import os
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
    
    # Canlı test için enstrümanlara göre sesler
    audio_urls = {
        'piano': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
        'guitar': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
        'flute': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
        'baglama': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
        'kaval': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'
    }
    
    selected_audio = audio_urls.get(instrument, audio_urls['piano'])
    
    return jsonify({
        'message': f'Canlı bulut sunucusunda işlendi ve {instrument.upper()} formatına hazırlandı!',
        'audio_url': selected_audio,
        'instrument': instrument
    })

if __name__ == '__main__':
    # Render'ın kendi atayacağı portu otomatik okuması için gerekli ayar
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
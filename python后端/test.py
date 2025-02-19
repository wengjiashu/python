from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import io
import base64
import emotion
import image_generate
import image_keywords
import link_mysql

app = Flask(__name__)
# 允许所有来源访问
CORS(app)  

@app.route('/main', methods=['POST'])
def main():
    try:
        # 从前端获取小朋友的输入
        data = request.get_json()
        message = data.get('emo', "I'm happy")
        print(message)
        # 调用函数得到情感关键词
        emo = emotion.emo_transform(message)
        print(emo)
        # 将关键词放入词库中搜索
        keywords_list = image_keywords.choose_keywords(emo)
        keywords = ','.join(keywords_list)
        print(keywords)
        # 将关键词作为生图参数
        img_io = image_generate.generate_image(keywords)
        print(img_io)
        if img_io:
            # 获取图像的二进制数据 存入 mysql
            image_data = img_io.getvalue()
            link_mysql.save_mysql(image_data, message)
            return send_file(img_io, mimetype='image/png')
        else:
            return jsonify({"error": "No images generated"}), 400
    except Exception as e:
        print(f"Error in main route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/history-images', methods=['GET'])
def history_images():
    try:
        images = link_mysql.get_history_images()
        return jsonify(images)
    except Exception as e:
        print(f"Error in history-images route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image_data = link_mysql.get_image_by_id(image_id)
        if image_data:
            img_io = io.BytesIO(image_data)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png')
        else:
            return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        print(f"Error in get_image route: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/save', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_data = data.get('imageData')
        image_name = data.get('imageName')  # 获取图片名称
        if not image_name:
            return jsonify({"error": "Missing image name"}), 400
        # 去除 data URI 前缀
        image_data = image_data.split(',')[1]
        # 解码 base64 数据
        decoded_image = base64.b64decode(image_data)
        # 保存到数据库，传递图片名称
        link_mysql.save_edited_image(decoded_image, image_name)
        return jsonify({"message": "Image saved successfully"}), 200
    except Exception as e:
        print(f"Error in save_image route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
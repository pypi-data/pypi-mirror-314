/*
 * SUDIO - Audio Processing Platform
 * Copyright (C) 2024 Hossein Zahaki
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 *  any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 *
 * - GitHub: https://github.com/MrZahaki/sudio
 */

#include "codec.hpp"
#include <stdexcept>
#include <cstring>
#include <cstdlib>
#include <ctime>
#include <fstream>

extern "C" {
    #include <lame.h>
    #include <FLAC/stream_encoder.h>
    #include <vorbis/vorbisenc.h>
    #include <vorbis/codec.h>
    #include <vorbis/vorbisfile.h>
}


namespace suio{



std::vector<uint8_t> AudioCodec::decodeAudioFile(const std::string& filename,
                                                 ma_format format,
                                                 uint32_t nchannels,
                                                 uint32_t sampleRate,
                                                 ma_dither_mode dither) {

    if (filename.substr(filename.find_last_of(".") + 1) == "ogg") {
        return decodeVorbisFile(filename, format, nchannels, sampleRate);
    }
    
    ma_decoder_config config = ma_decoder_config_init(format, nchannels, sampleRate);
    config.ditherMode = dither;

    ma_uint64 frameCount;
    void* pSampleData;
    ma_result result = ma_decode_file(filename.c_str(), &config, &frameCount, &pSampleData);

    if (result != MA_SUCCESS) {
        throw std::runtime_error("Failed to decode file");
    }

    size_t dataSize = frameCount * nchannels * ma_get_bytes_per_sample(format);
    std::vector<uint8_t> decodedData(static_cast<uint8_t*>(pSampleData),
                                     static_cast<uint8_t*>(pSampleData) + dataSize);

    ma_free(pSampleData, nullptr);

    return decodedData;
}


std::vector<uint8_t> AudioCodec::decodeVorbisFile(const std::string& filename,
                                                  ma_format format,
                                                  uint32_t nchannels,
                                                  uint32_t sampleRate) {
    OggVorbis_File vf;
    if (ov_fopen(filename.c_str(), &vf) != 0) {
        throw std::runtime_error("Failed to open Vorbis file");
    }

    vorbis_info* vi = ov_info(&vf, -1);
    if (!vi) {
        ov_clear(&vf);
        throw std::runtime_error("Failed to get Vorbis file info");
    }

    std::vector<float> decodedFloat;
    int bitStream;
    constexpr int bufferSize = 4096;
    float** buffer;

    while (true) {
        long bytesRead = ov_read_float(&vf, &buffer, bufferSize, &bitStream);
        if (bytesRead == 0) {
            break; // End of file
        } else if (bytesRead < 0) {
            ov_clear(&vf);
            throw std::runtime_error("Error reading Vorbis file");
        }

        for (int i = 0; i < bytesRead; ++i) {
            for (int j = 0; j < vi->channels; ++j) {
                decodedFloat.push_back(buffer[j][i]);
            }
        }
    }

    if (static_cast<uint32_t>(vi->rate) != sampleRate || static_cast<uint32_t>(vi->channels) != nchannels) {
        ma_resampler_config config = ma_resampler_config_init(
            ma_format_f32,
            vi->channels,
            vi->rate,
            sampleRate,
            ma_resample_algorithm_linear);

        ma_resampler resampler;
        ma_result result = ma_resampler_init(&config, nullptr, &resampler);
        if (result != MA_SUCCESS) {
            throw std::runtime_error("Failed to initialize resampler");
        }

        ma_uint64 frameCountIn = decodedFloat.size() / vi->channels;
        ma_uint64 frameCountOut = (frameCountIn * sampleRate) / vi->rate; 
        
        std::vector<float> resampledFloat(frameCountOut * nchannels);
        ma_uint64 framesRead = frameCountIn;
        ma_uint64 framesWritten = frameCountOut;
        
        result = ma_resampler_process_pcm_frames(&resampler, decodedFloat.data(), &framesRead, resampledFloat.data(), &framesWritten);
        if (result != MA_SUCCESS) {
            ma_resampler_uninit(&resampler, nullptr);
            throw std::runtime_error("Failed to resample audio data");
        }

        ma_resampler_uninit(&resampler, nullptr);
        decodedFloat = std::move(resampledFloat);
    }

    // Convert to desired format
    std::vector<uint8_t> decodedData(decodedFloat.size() * ma_get_bytes_per_sample(format));
    ma_convert_pcm_frames_format(decodedData.data(), format, decodedFloat.data(), ma_format_f32, decodedFloat.size() / nchannels, nchannels, ma_dither_mode_triangle);

    ov_clear(&vf);

    return decodedData;
}


std::vector<uint8_t> AudioCodec::encodeToWav(
        const std::vector<uint8_t>& data,
        ma_format format,
        uint32_t nchannels,
        uint32_t sampleRate) {
        
        ma_encoder encoder;
        std::vector<uint8_t> encodedData;
        ma_uint64 framesWritten;
        
        // encoder configuration
        ma_encoder_config config = ma_encoder_config_init(
            ma_encoding_format_wav,
            format,
            nchannels,
            sampleRate
        );

        // write callback
        ma_encoder_write_proc onWrite = [](ma_encoder* pEncoder, const void* pBufferIn, size_t bytesToWrite, size_t* pBytesWritten) -> ma_result {
            auto* buffer = static_cast<std::vector<uint8_t>*>(pEncoder->pUserData);
            const uint8_t* byteData = static_cast<const uint8_t*>(pBufferIn);
            buffer->insert(buffer->end(), byteData, byteData + bytesToWrite);
            *pBytesWritten = bytesToWrite;
            return MA_SUCCESS;
        };

        // seek callback
        ma_encoder_seek_proc onSeek = [](ma_encoder* pEncoder, ma_int64 offset, ma_seek_origin origin) -> ma_result {
            return MA_SUCCESS; // Allow seeking 
        };

        ma_result result = ma_encoder_init(
            onWrite,
            onSeek,
            &encodedData,  
            &config,
            &encoder
        );

        if (result != MA_SUCCESS) {
            throw std::runtime_error("Failed to initialize WAV encoder");
        }

        ma_uint64 frameCount = data.size() / (nchannels * ma_get_bytes_per_sample(format));

        result = ma_encoder_write_pcm_frames(&encoder, data.data(), frameCount, &framesWritten);
        
        if (result != MA_SUCCESS) {
            ma_encoder_uninit(&encoder);
            throw std::runtime_error("Failed to encode WAV data");
        }

        if (framesWritten != frameCount) {
            ma_encoder_uninit(&encoder);
            throw std::runtime_error("Failed to write all frames");
        }

        // Cleanup
        ma_encoder_uninit(&encoder);
        return encodedData;
    }



uint64_t AudioCodec::encodeWavFile(const std::string& filename,
                              const std::vector<uint8_t>& data,
                              ma_format format,
                              uint32_t nchannels,
                              uint32_t sampleRate) {

    ma_encoder encoder;
    ma_uint64 framesWritten;


    ma_encoder_config config = ma_encoder_config_init(
        ma_encoding_format_wav, 
        format, 
        nchannels, 
        sampleRate
        );

    ma_result result = ma_encoder_init_file(filename.c_str(), &config, &encoder);
    if (result != MA_SUCCESS) {
        throw std::runtime_error("Failed to prepare file for encoding into WAV format");
    }
    
    // Calculate the number of frames
    ma_uint64 frameCount = data.size() / (nchannels * ma_get_bytes_per_sample(format));

    result = ma_encoder_write_pcm_frames(&encoder, data.data(), frameCount, &framesWritten);
    if (result != MA_SUCCESS) {
        throw std::runtime_error("Failed to encoding WAV into format");
    }

    if (framesWritten != frameCount) {
        throw std::runtime_error("Failed to write all frames");
    }
    ma_encoder_uninit(&encoder);

    return framesWritten;
}


uint64_t AudioCodec::encodeMP3File(const std::string& filename,
                                   const std::vector<uint8_t>& data,
                                   ma_format format,
                                   uint32_t nchannels,
                                   uint32_t sampleRate,
                                   int bitrate,
                                   int quality
                                   ) {
    lame_t lame = lame_init();
    if (!lame) {
        throw std::runtime_error("Failed to initialize LAME encoder");
    }

    lame_set_num_channels(lame, nchannels);
    lame_set_in_samplerate(lame, sampleRate);
    lame_set_brate(lame, bitrate);
    lame_set_quality(lame, quality); 

    if (lame_init_params(lame) < 0) {
        lame_close(lame);
        throw std::runtime_error("Failed to set LAME parameters");
    }

    FILE* mp3File = fopen(filename.c_str(), "wb");
    if (!mp3File) {
        lame_close(lame);
        throw std::runtime_error("Failed to open output MP3 file");
    }

    const int PCM_SIZE = 8192;
    const int MP3_SIZE = 8192;
    std::vector<float> pcm_buffer(PCM_SIZE * 2);
    unsigned char mp3_buffer[MP3_SIZE];

    uint64_t totalFramesWritten = 0;
    size_t bytesPerSample = ma_get_bytes_per_sample(format);
    size_t frameSize = nchannels * bytesPerSample;
    size_t totalFrames = data.size() / frameSize;

    for (size_t i = 0; i < totalFrames; i += PCM_SIZE) {
        size_t framesToProcess = std::min(static_cast<size_t>(PCM_SIZE), totalFrames - i);
        
        // Convert input data to float
        for (size_t j = 0; j < framesToProcess * nchannels; ++j) {
            size_t dataIndex = (i * frameSize) + (j * bytesPerSample);
            float sample;
            switch (format) {
                case ma_format_u8:
                    sample = (*reinterpret_cast<const uint8_t*>(&data[dataIndex]) - 128) / 128.0f;
                    break;
                case ma_format_s16:
                    sample = *reinterpret_cast<const int16_t*>(&data[dataIndex]) / 32768.0f;
                    break;
                case ma_format_s24: {
                    int32_t sample24 = (data[dataIndex] << 8) | (data[dataIndex + 1] << 16) | (data[dataIndex + 2] << 24);
                    sample = static_cast<float>(sample24) / 8388608.0f;
                    break;
                }
                case ma_format_s32:
                    sample = *reinterpret_cast<const int32_t*>(&data[dataIndex]) / 2147483648.0f;
                    break;
                case ma_format_f32:
                    sample = *reinterpret_cast<const float*>(&data[dataIndex]);
                    break;
                default:
                    throw std::runtime_error("Unsupported sample format");
            }
            pcm_buffer[j] = sample;
        }

        int bytesEncoded;
        if (nchannels == 1) {
            bytesEncoded = lame_encode_buffer_ieee_float(lame, pcm_buffer.data(), nullptr, framesToProcess, mp3_buffer, MP3_SIZE);
        } else {
            bytesEncoded = lame_encode_buffer_interleaved_ieee_float(lame, pcm_buffer.data(), framesToProcess, mp3_buffer, MP3_SIZE);
        }

        if (bytesEncoded < 0) {
            fclose(mp3File);
            lame_close(lame);
            throw std::runtime_error("MP3 encoding failed");
        }

        fwrite(mp3_buffer, 1, bytesEncoded, mp3File);
        totalFramesWritten += framesToProcess;
    }

    int flush_result = lame_encode_flush(lame, mp3_buffer, MP3_SIZE);
    if (flush_result > 0) {
        fwrite(mp3_buffer, 1, flush_result, mp3File);
    }

    fclose(mp3File);
    lame_close(lame);

    return totalFramesWritten;
}

std::vector<uint8_t> AudioCodec::encodeToMP3(
    const std::vector<uint8_t>& data,
    ma_format format,
    uint32_t nchannels,
    uint32_t sampleRate,
    int bitrate = 128,
    int quality = 2) {
    
    lame_t lame = lame_init();
    if (!lame) {
        throw std::runtime_error("Failed to initialize LAME encoder");
    }

    lame_set_num_channels(lame, nchannels);
    lame_set_in_samplerate(lame, sampleRate);
    lame_set_brate(lame, bitrate);
    lame_set_quality(lame, quality);

    if (lame_init_params(lame) < 0) {
        lame_close(lame);
        throw std::runtime_error("Failed to set LAME parameters");
    }

    std::vector<uint8_t> mp3Data;
    const int PCM_SIZE = 8192;
    const int MP3_SIZE = 8192;
    std::vector<float> pcm_buffer(PCM_SIZE * 2);
    std::vector<uint8_t> mp3_buffer(MP3_SIZE);

    size_t bytesPerSample = ma_get_bytes_per_sample(format);
    size_t frameSize = nchannels * bytesPerSample;
    size_t totalFrames = data.size() / frameSize;

    for (size_t i = 0; i < totalFrames; i += PCM_SIZE) {
        size_t framesToProcess = std::min(static_cast<size_t>(PCM_SIZE), totalFrames - i);
        
        // Convert input data to float
        for (size_t j = 0; j < framesToProcess * nchannels; ++j) {
            size_t dataIndex = (i * frameSize) + (j * bytesPerSample);
            float sample;
            switch (format) {
                case ma_format_u8:
                    sample = (*reinterpret_cast<const uint8_t*>(&data[dataIndex]) - 128) / 128.0f;
                    break;
                case ma_format_s16:
                    sample = *reinterpret_cast<const int16_t*>(&data[dataIndex]) / 32768.0f;
                    break;
                case ma_format_s24: {
                    int32_t sample24 = (data[dataIndex] << 8) | (data[dataIndex + 1] << 16) | (data[dataIndex + 2] << 24);
                    sample = static_cast<float>(sample24) / 8388608.0f;
                    break;
                }
                case ma_format_s32:
                    sample = *reinterpret_cast<const int32_t*>(&data[dataIndex]) / 2147483648.0f;
                    break;
                case ma_format_f32:
                    sample = *reinterpret_cast<const float*>(&data[dataIndex]);
                    break;
                default:
                    throw std::runtime_error("Unsupported sample format");
            }
            pcm_buffer[j] = sample;
        }

        int bytesEncoded;
        if (nchannels == 1) {
            bytesEncoded = lame_encode_buffer_ieee_float(lame, pcm_buffer.data(), nullptr, framesToProcess, mp3_buffer.data(), MP3_SIZE);
        } else {
            bytesEncoded = lame_encode_buffer_interleaved_ieee_float(lame, pcm_buffer.data(), framesToProcess, mp3_buffer.data(), MP3_SIZE);
        }

        if (bytesEncoded < 0) {
            lame_close(lame);
            throw std::runtime_error("MP3 encoding failed");
        }

        mp3Data.insert(mp3Data.end(), mp3_buffer.begin(), mp3_buffer.begin() + bytesEncoded);
    }

    // Flush the encoder
    std::vector<uint8_t> flush_buffer(MP3_SIZE);
    int flush_result = lame_encode_flush(lame, flush_buffer.data(), MP3_SIZE);
    if (flush_result > 0) {
        mp3Data.insert(mp3Data.end(), flush_buffer.begin(), flush_buffer.begin() + flush_result);
    }

    lame_close(lame);
    return mp3Data;
}


uint64_t AudioCodec::encodeFlacFile(const std::string& filename,
                                    const std::vector<uint8_t>& data,
                                    ma_format format,
                                    uint32_t nchannels,
                                    uint32_t sampleRate,
                                    int compressionLevel) {
    FLAC__StreamEncoder *encoder = FLAC__stream_encoder_new();
    if (!encoder) {
        throw std::runtime_error("Failed to create FLAC encoder");
    }

    FLAC__stream_encoder_set_channels(encoder, nchannels);
    FLAC__stream_encoder_set_bits_per_sample(encoder, ma_get_bytes_per_sample(format) * 8);
    FLAC__stream_encoder_set_sample_rate(encoder, sampleRate);
    FLAC__stream_encoder_set_compression_level(encoder, compressionLevel);

    FLAC__StreamEncoderInitStatus init_status = FLAC__stream_encoder_init_file(encoder, filename.c_str(), nullptr, nullptr);
    if (init_status != FLAC__STREAM_ENCODER_INIT_STATUS_OK) {
        FLAC__stream_encoder_delete(encoder);
        throw std::runtime_error("Failed to initialize FLAC encoder");
    }

    size_t bytesPerSample = ma_get_bytes_per_sample(format);
    size_t frameSize = nchannels * bytesPerSample;
    size_t totalFrames = data.size() / frameSize;

    std::vector<FLAC__int32> samples(nchannels * totalFrames);

    // Convert input data to FLAC__int32
    for (size_t i = 0; i < totalFrames; ++i) {
        for (uint32_t j = 0; j < nchannels; ++j) {
            size_t dataIndex = i * frameSize + j * bytesPerSample;
            FLAC__int32 sample;
            switch (format) {
                case ma_format_u8:
                    sample = static_cast<FLAC__int32>(*reinterpret_cast<const uint8_t*>(&data[dataIndex])) - 128;
                    break;
                case ma_format_s16:
                    sample = static_cast<FLAC__int32>(*reinterpret_cast<const int16_t*>(&data[dataIndex]));
                    break;
                case ma_format_s24: {
                    int32_t sample24 = (data[dataIndex] << 8) | (data[dataIndex + 1] << 16) | (data[dataIndex + 2] << 24);
                    sample = sample24 >> 8;
                    break;
                }
                case ma_format_s32:
                    sample = static_cast<FLAC__int32>(*reinterpret_cast<const int32_t*>(&data[dataIndex]));
                    break;
                case ma_format_f32:
                    sample = static_cast<FLAC__int32>(*reinterpret_cast<const float*>(&data[dataIndex]) * 8388607.0f);
                    break;
                default:
                    throw std::runtime_error("Unsupported sample format for FLAC encoding");
            }
            samples[i * nchannels + j] = sample;
        }
    }

    FLAC__bool ok = FLAC__stream_encoder_process_interleaved(encoder, samples.data(), totalFrames);
    
    FLAC__stream_encoder_finish(encoder);
    FLAC__stream_encoder_delete(encoder);

    if (!ok) {
        throw std::runtime_error("FLAC encoding failed");
    }

    return totalFrames;
}


uint64_t AudioCodec::encodeVorbisFile(const std::string& filename,
                                      const std::vector<uint8_t>& data,
                                      ma_format format,
                                      uint32_t nchannels,
                                      uint32_t sampleRate,
                                      float quality) {
    vorbis_info vi;
    vorbis_comment vc;
    vorbis_dsp_state vd;
    vorbis_block vb;
    ogg_stream_state os;
    ogg_page og;
    ogg_packet op;

    vorbis_info_init(&vi);
    if (vorbis_encode_init_vbr(&vi, nchannels, sampleRate, quality) != 0) {
        throw std::runtime_error("Failed to initialize Vorbis encoder");
    }

    vorbis_comment_init(&vc);
    vorbis_comment_add_tag(&vc, "ENCODER", "AudioCodec");

    vorbis_analysis_init(&vd, &vi);
    vorbis_block_init(&vd, &vb);

    srand(time(NULL));
    ogg_stream_init(&os, rand());

    std::ofstream oggFile(filename, std::ios::binary);
    if (!oggFile) {
        throw std::runtime_error("Failed to open output Ogg file");
    }

    // Write header
    {
        ogg_packet header;
        ogg_packet header_comm;
        ogg_packet header_code;

        vorbis_analysis_headerout(&vd, &vc, &header, &header_comm, &header_code);
        ogg_stream_packetin(&os, &header);
        ogg_stream_packetin(&os, &header_comm);
        ogg_stream_packetin(&os, &header_code);

        while (ogg_stream_flush(&os, &og) != 0) {
            oggFile.write(reinterpret_cast<char*>(og.header), og.header_len);
            oggFile.write(reinterpret_cast<char*>(og.body), og.body_len);
        }
    }

    size_t bytesPerSample = ma_get_bytes_per_sample(format);
    size_t frameSize = nchannels * bytesPerSample;
    size_t totalFrames = data.size() / frameSize;
    uint64_t totalFramesWritten = 0;

    const int BUFFER_SIZE = 1024;
    std::vector<float> pcmBuffer(BUFFER_SIZE * nchannels);

    for (size_t i = 0; i < totalFrames; i += BUFFER_SIZE) {
        size_t framesToProcess = std::min(static_cast<size_t>(BUFFER_SIZE), totalFrames - i);
        
        // Convert  data to float
        for (size_t j = 0; j < framesToProcess; ++j) {
            for (uint32_t k = 0; k < nchannels; ++k) {
                size_t dataIndex = (i + j) * frameSize + k * bytesPerSample;
                float sample = 0.0f;
                switch (format) {
                    case ma_format_u8:
                        sample = (data[dataIndex] - 128) / 128.0f;
                        break;
                    case ma_format_s16:
                        sample = *reinterpret_cast<const int16_t*>(&data[dataIndex]) / 32768.0f;
                        break;
                    case ma_format_s24: {
                        int32_t sample24 = (data[dataIndex] << 8) | (data[dataIndex + 1] << 16) | (data[dataIndex + 2] << 24);
                        sample = static_cast<float>(sample24) / 8388608.0f;
                        break;
                    }
                    case ma_format_s32:
                        sample = *reinterpret_cast<const int32_t*>(&data[dataIndex]) / 2147483648.0f;
                        break;
                    case ma_format_f32:
                        sample = *reinterpret_cast<const float*>(&data[dataIndex]);
                        break;
                    default:
                        throw std::runtime_error("Unsupported sample format for Vorbis encoding");
                }
                pcmBuffer[j * nchannels + k] = sample;
            }
        }

        float **buffer = vorbis_analysis_buffer(&vd, framesToProcess);
        for (uint32_t k = 0; k < nchannels; ++k) {
            for (size_t j = 0; j < framesToProcess; ++j) {
                buffer[k][j] = pcmBuffer[j * nchannels + k];
            }
        }

        vorbis_analysis_wrote(&vd, framesToProcess);
        totalFramesWritten += framesToProcess;

        while (vorbis_analysis_blockout(&vd, &vb) == 1) {
            vorbis_analysis(&vb, NULL);
            vorbis_bitrate_addblock(&vb);

            while (vorbis_bitrate_flushpacket(&vd, &op)) {
                ogg_stream_packetin(&os, &op);

                while (ogg_stream_pageout(&os, &og) != 0) {
                    oggFile.write(reinterpret_cast<char*>(og.header), og.header_len);
                    oggFile.write(reinterpret_cast<char*>(og.body), og.body_len);
                }
            }
        }
    }

    // Flush remaining data
    vorbis_analysis_wrote(&vd, 0);
    while (vorbis_analysis_blockout(&vd, &vb) == 1) {
        vorbis_analysis(&vb, NULL);
        vorbis_bitrate_addblock(&vb);

        while (vorbis_bitrate_flushpacket(&vd, &op)) {
            ogg_stream_packetin(&os, &op);

            while (ogg_stream_pageout(&os, &og) != 0) {
                oggFile.write(reinterpret_cast<char*>(og.header), og.header_len);
                oggFile.write(reinterpret_cast<char*>(og.body), og.body_len);
            }
        }
    }

    // Ensure  data is written
    while (ogg_stream_flush(&os, &og) != 0) {
        oggFile.write(reinterpret_cast<char*>(og.header), og.header_len);
        oggFile.write(reinterpret_cast<char*>(og.body), og.body_len);
    }

    ogg_stream_clear(&os);
    vorbis_block_clear(&vb);
    vorbis_dsp_clear(&vd);
    vorbis_comment_clear(&vc);
    vorbis_info_clear(&vi);

    oggFile.close();

    return totalFramesWritten;
}


AudioFileInfo AudioCodec::getFileInfo(const std::string& filename) {
    AudioFileInfo info;
    info.name = filename;
    
    std::string ext = filename.substr(filename.find_last_of(".") + 1);
    if (ext == "wav") info.fileFormat = FileFormat::WAV;
    else if (ext == "mp3") info.fileFormat = FileFormat::MP3;
    else if (ext == "flac") info.fileFormat = FileFormat::FLAC;
    else if (ext == "ogg") info.fileFormat = FileFormat::VORBIS;
    else info.fileFormat = FileFormat::UNKNOWN;

    // Handle Vorbis files separately
    if (info.fileFormat == FileFormat::VORBIS) {
        OggVorbis_File vf;
        if (ov_fopen(filename.c_str(), &vf) != 0) {
            throw std::runtime_error("Failed to open Vorbis file");
        }

        vorbis_info* vi = ov_info(&vf, -1);
        if (!vi) {
            ov_clear(&vf);
            throw std::runtime_error("Failed to get Vorbis file info");
        }

        info.nchannels = vi->channels;
        info.sampleRate = vi->rate;
        info.sampleFormat = ma_format_f32; // Vorbis uses float internally
        info.numFrames = ov_pcm_total(&vf, -1);
        info.duration = static_cast<float>(info.numFrames) / info.sampleRate;

        ov_clear(&vf);
    } else {
        ma_decoder decoder;
        ma_result result = ma_decoder_init_file(filename.c_str(), nullptr, &decoder);
        
        if (result != MA_SUCCESS) {
            std::string errorMsg = "Failed to open file: " + filename + ". Error code: " + std::to_string(result);
            switch (result) {
                case MA_INVALID_FILE:
                    errorMsg += " (Invalid file)";
                    break;
                case MA_FORMAT_NOT_SUPPORTED:
                    errorMsg += " (Invalid format)";
                    break;
                case MA_NOT_IMPLEMENTED:
                    errorMsg += " (Format not supported)";
                    break;
            }
            throw std::runtime_error(errorMsg);
        }

        info.nchannels = decoder.outputChannels;
        info.sampleRate = decoder.outputSampleRate;
        info.sampleFormat = decoder.outputFormat;
        ma_uint64 frameCount;
        ma_decoder_get_length_in_pcm_frames(&decoder, &frameCount);
        info.numFrames = frameCount;
        info.duration = static_cast<float>(info.numFrames) / info.sampleRate;

        ma_decoder_uninit(&decoder);
    }

    return info;
}

std::unique_ptr<ma_decoder> AudioCodec::initializeDecoder(const std::string& filename,
                                                          ma_format outputFormat,
                                                          uint32_t nchannels,
                                                          uint32_t sampleRate,
                                                          ma_dither_mode dither) {
    auto decoder = std::make_unique<ma_decoder>();
    ma_decoder_config config = ma_decoder_config_init(outputFormat, nchannels, sampleRate);
    config.ditherMode = dither;

    ma_result result = ma_decoder_init_file(filename.c_str(), &config, decoder.get());
    if (result != MA_SUCCESS) {
        throw std::runtime_error("Failed to initialize decoder");
    }

    return decoder;
}

std::vector<uint8_t> AudioCodec::readDecoderFrames(ma_decoder* decoder, uint64_t framesToRead) {
    std::vector<uint8_t> buffer(framesToRead * decoder->outputChannels * ma_get_bytes_per_sample(decoder->outputFormat));
    ma_uint64 framesRead;
    ma_result result = ma_decoder_read_pcm_frames(decoder, buffer.data(), framesToRead, &framesRead);
    
    if (result != MA_SUCCESS) {
        throw std::runtime_error("Failed to read PCM frames");
    }

    buffer.resize(framesRead * decoder->outputChannels * ma_get_bytes_per_sample(decoder->outputFormat));
    return buffer;
}

AudioCodec::AudioFileStream::AudioFileStream(const std::string& filename,
                                             ma_format outputFormat,
                                             uint32_t nchannels,
                                             uint32_t sampleRate,
                                             uint64_t framesToRead,
                                             ma_dither_mode dither,
                                             uint64_t seekFrame)
    : m_framesToRead(framesToRead), m_nchannels(nchannels), m_outputFormat(outputFormat) {
    m_decoder = AudioCodec::initializeDecoder(filename, outputFormat, nchannels, sampleRate, dither);
    
    if (seekFrame > 0) {
        ma_result result = ma_decoder_seek_to_pcm_frame(m_decoder.get(), seekFrame);
        if (result != MA_SUCCESS) {
            throw std::runtime_error("Failed to seek to frame");
        }
    }
}

AudioCodec::AudioFileStream::~AudioFileStream() {
    ma_decoder_uninit(m_decoder.get());
}

std::vector<uint8_t> AudioCodec::AudioFileStream::readFrames(uint64_t framesToRead) {
    if (framesToRead == 0) {
        framesToRead = m_framesToRead;
    }
    return AudioCodec::readDecoderFrames(m_decoder.get(), framesToRead);
}


}

